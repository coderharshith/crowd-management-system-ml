"""
Social Distancing Detection Module
Calculates distances between detected persons and identifies violations.
"""
import numpy as np
import cv2
import math
from typing import List, Tuple, Dict


def calculate_distance(person1: Tuple[int, int, int, int], person2: Tuple[int, int, int, int]) -> float:
    """
    Calculate Euclidean distance between centers of two bounding boxes.
    
    Args:
        person1: (x1, y1, x2, y2) bounding box
        person2: (x1, y1, x2, y2) bounding box
    
    Returns:
        Distance in pixels between the two persons
    """
    cx1 = (person1[0] + person1[2]) / 2
    cy1 = (person1[1] + person1[3]) / 2
    cx2 = (person2[0] + person2[2]) / 2
    cy2 = (person2[1] + person2[3]) / 2
    
    distance = math.sqrt((cx2 - cx1)**2 + (cy2 - cy1)**2)
    return distance


def detect_violations(persons: List[Tuple[int, int, int, int, float]], 
                     min_distance: float) -> List[Dict]:
    """
    Detect social distancing violations among detected persons.
    
    Args:
        persons: List of (x1, y1, x2, y2, conf) tuples
        min_distance: Minimum allowed distance in pixels
    
    Returns:
        List of violation dictionaries with person pairs and distance
    """
    violations = []
    
    for i in range(len(persons)):
        for j in range(i + 1, len(persons)):
            distance = calculate_distance(persons[i][:4], persons[j][:4])
            
            if distance < min_distance:
                violations.append({
                    'person1_idx': i,
                    'person2_idx': j,
                    'person1_box': persons[i][:4],
                    'person2_box': persons[j][:4],
                    'distance': round(distance, 2),
                    'violation_severity': 'high' if distance < min_distance * 0.5 else 'medium'
                })
    
    return violations


def draw_violation_lines(frame: np.ndarray, violations: List[Dict], 
                         persons: List[Tuple[int, int, int, int, float]]) -> np.ndarray:
    """
    Draw visual indicators for social distancing violations on the frame.
    
    Args:
        frame: Video frame to draw on
        violations: List of violation dictionaries
        persons: List of detected persons
    
    Returns:
        Frame with violation lines drawn
    """
    for violation in violations:
        # Get centers of both persons
        box1 = violation['person1_box']
        box2 = violation['person2_box']
        
        cx1 = int((box1[0] + box1[2]) / 2)
        cy1 = int((box1[1] + box1[3]) / 2)
        cx2 = int((box2[0] + box2[2]) / 2)
        cy2 = int((box2[1] + box2[3]) / 2)
        
        # Color based on severity
        color = (0, 0, 255) if violation['violation_severity'] == 'high' else (0, 165, 255)
        
        # Draw line between persons
        cv2.line(frame, (cx1, cy1), (cx2, cy2), color, 2)
        
        # Draw circles at centers
        cv2.circle(frame, (cx1, cy1), 5, color, -1)
        cv2.circle(frame, (cx2, cy2), 5, color, -1)
        
        # Draw distance text at midpoint
        mid_x = int((cx1 + cx2) / 2)
        mid_y = int((cy1 + cy2) / 2)
        cv2.putText(frame, f"{violation['distance']:.0f}px", 
                   (mid_x, mid_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                   0.5, color, 2)
    
    return frame


def draw_safe_zones(frame: np.ndarray, persons: List[Tuple[int, int, int, int, float]], 
                    min_distance: float) -> np.ndarray:
    """
    Draw circles around each person showing the minimum safe distance.
    
    Args:
        frame: Video frame to draw on
        persons: List of detected persons
        min_distance: Minimum safe distance in pixels
    
    Returns:
        Frame with safe zone circles drawn
    """
    for person in persons:
        cx = int((person[0] + person[2]) / 2)
        cy = int((person[1] + person[3]) / 2)
        
        # Draw semi-transparent circle
        overlay = frame.copy()
        cv2.circle(overlay, (cx, cy), int(min_distance), (0, 255, 0), 1)
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
    
    return frame


def get_violation_summary(violations: List[Dict]) -> Dict:
    """
    Generate summary statistics for social distancing violations.
    
    Args:
        violations: List of violation dictionaries
    
    Returns:
        Dictionary with violation statistics
    """
    if not violations:
        return {
            'total_violations': 0,
            'high_severity': 0,
            'medium_severity': 0,
            'avg_distance': 0,
            'min_distance': 0
        }
    
    high_severity = sum(1 for v in violations if v['violation_severity'] == 'high')
    medium_severity = len(violations) - high_severity
    avg_distance = sum(v['distance'] for v in violations) / len(violations)
    min_distance = min(v['distance'] for v in violations)
    
    return {
        'total_violations': len(violations),
        'high_severity': high_severity,
        'medium_severity': medium_severity,
        'avg_distance': round(avg_distance, 2),
        'min_distance': round(min_distance, 2)
    }
