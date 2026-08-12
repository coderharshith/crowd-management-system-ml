"""
Abnormal Activity Detection Module
Tracks person movements and detects unusual crowd behaviors.
"""
import numpy as np
import cv2
import time
from typing import List, Tuple, Dict, Optional
from collections import defaultdict, deque


class PersonTracker:
    """Tracks individual person movements across frames."""
    
    def __init__(self, max_history: int = 30):
        self.tracks = defaultdict(lambda: deque(maxlen=max_history))
        self.next_id = 0
        self.max_distance_for_match = 100  # pixels
        
    def update(self, persons: List[Tuple[int, int, int, int, float]], timestamp: float):
        """
        Update tracking with new detections.
        
        Args:
            persons: List of (x1, y1, x2, y2, conf) tuples
            timestamp: Current timestamp
        
        Returns:
            Dictionary mapping person_id to current position
        """
        current_positions = {}
        
        # Calculate centers
        centers = []
        for person in persons:
            cx = (person[0] + person[2]) / 2
            cy = (person[1] + person[3]) / 2
            centers.append((cx, cy))
        
        # Match with existing tracks
        matched_ids = set()
        for i, center in enumerate(centers):
            best_match_id = None
            best_distance = float('inf')
            
            # Find closest existing track
            for track_id, track_history in self.tracks.items():
                if track_id in matched_ids:
                    continue
                if len(track_history) == 0:
                    continue
                    
                last_pos = track_history[-1]['position']
                distance = np.sqrt((center[0] - last_pos[0])**2 + (center[1] - last_pos[1])**2)
                
                if distance < best_distance and distance < self.max_distance_for_match:
                    best_distance = distance
                    best_match_id = track_id
            
            # Assign to track
            if best_match_id is not None:
                person_id = best_match_id
                matched_ids.add(person_id)
            else:
                person_id = self.next_id
                self.next_id += 1
            
            # Add to track
            self.tracks[person_id].append({
                'position': center,
                'timestamp': timestamp,
                'bbox': persons[i][:4]
            })
            current_positions[person_id] = center
        
        # Clean old tracks (not seen in last 5 seconds)
        current_time = timestamp
        to_remove = []
        for track_id, track_history in self.tracks.items():
            if len(track_history) > 0:
                last_seen = track_history[-1]['timestamp']
                if current_time - last_seen > 5.0:
                    to_remove.append(track_id)
        
        for track_id in to_remove:
            del self.tracks[track_id]
        
        return current_positions
    
    def get_velocity(self, person_id: int) -> Optional[Tuple[float, float]]:
        """Calculate velocity for a person (pixels per second)."""
        if person_id not in self.tracks or len(self.tracks[person_id]) < 2:
            return None
        
        track = self.tracks[person_id]
        recent = list(track)[-5:]  # Use last 5 positions
        
        if len(recent) < 2:
            return None
        
        # Calculate average velocity
        total_dx = 0
        total_dy = 0
        total_dt = 0
        
        for i in range(1, len(recent)):
            dx = recent[i]['position'][0] - recent[i-1]['position'][0]
            dy = recent[i]['position'][1] - recent[i-1]['position'][1]
            dt = recent[i]['timestamp'] - recent[i-1]['timestamp']
            
            if dt > 0:
                total_dx += dx
                total_dy += dy
                total_dt += dt
        
        if total_dt > 0:
            vx = total_dx / total_dt
            vy = total_dy / total_dt
            return (vx, vy)
        
        return None
    
    def get_speed(self, person_id: int) -> Optional[float]:
        """Calculate speed magnitude for a person."""
        velocity = self.get_velocity(person_id)
        if velocity is None:
            return None
        
        speed = np.sqrt(velocity[0]**2 + velocity[1]**2)
        return speed


def detect_sudden_movement(tracker: PersonTracker, threshold: float = 80) -> List[Dict]:
    """
    Detect persons moving suddenly (high velocity).
    
    Args:
        tracker: PersonTracker instance
        threshold: Speed threshold in pixels/second
    
    Returns:
        List of sudden movement events
    """
    events = []
    
    for person_id in tracker.tracks.keys():
        speed = tracker.get_speed(person_id)
        if speed is not None and speed > threshold:
            velocity = tracker.get_velocity(person_id)
            events.append({
                'type': 'sudden_movement',
                'person_id': person_id,
                'speed': round(speed, 2),
                'velocity': (round(velocity[0], 2), round(velocity[1], 2)),
                'severity': 'high' if speed > threshold * 1.5 else 'medium',
                'timestamp': time.time()
            })
    
    return events


def detect_crowd_rush(tracker: PersonTracker, rush_threshold: int = 5, 
                     velocity_threshold: float = 60) -> Optional[Dict]:
    """
    Detect if multiple people are moving quickly in similar direction (crowd rush).
    
    Args:
        tracker: PersonTracker instance
        rush_threshold: Minimum number of people moving for rush detection
        velocity_threshold: Minimum speed for rush
    
    Returns:
        Rush event dictionary or None
    """
    fast_movers = []
    
    for person_id in tracker.tracks.keys():
        speed = tracker.get_speed(person_id)
        velocity = tracker.get_velocity(person_id)
        
        if speed is not None and speed > velocity_threshold and velocity is not None:
            fast_movers.append({
                'person_id': person_id,
                'velocity': velocity,
                'speed': speed
            })
    
    if len(fast_movers) >= rush_threshold:
        # Calculate average direction
        avg_vx = sum(m['velocity'][0] for m in fast_movers) / len(fast_movers)
        avg_vy = sum(m['velocity'][1] for m in fast_movers) / len(fast_movers)
        avg_speed = sum(m['speed'] for m in fast_movers) / len(fast_movers)
        
        # Calculate direction angle
        angle = np.arctan2(avg_vy, avg_vx) * 180 / np.pi
        
        return {
            'type': 'crowd_rush',
            'num_people': len(fast_movers),
            'avg_speed': round(avg_speed, 2),
            'direction_angle': round(angle, 2),
            'severity': 'critical' if len(fast_movers) > rush_threshold * 2 else 'high',
            'timestamp': time.time()
        }
    
    return None


def detect_loitering(tracker: PersonTracker, loiter_time: float = 300) -> List[Dict]:
    """
    Detect persons staying in same area for extended time.
    
    Args:
        tracker: PersonTracker instance
        loiter_time: Time threshold in seconds
    
    Returns:
        List of loitering events
    """
    events = []
    current_time = time.time()
    
    for person_id, track in tracker.tracks.items():
        if len(track) < 10:
            continue
        
        # Check time span
        first_time = track[0]['timestamp']
        last_time = track[-1]['timestamp']
        duration = last_time - first_time
        
        if duration < loiter_time:
            continue
        
        # Check if person stayed in small area
        positions = [t['position'] for t in track]
        xs = [p[0] for p in positions]
        ys = [p[1] for p in positions]
        
        # Calculate bounding box of movement
        movement_width = max(xs) - min(xs)
        movement_height = max(ys) - min(ys)
        movement_area = movement_width * movement_height
        
        # If movement area is small, it's loitering
        if movement_area < 5000:  # 50x100 pixel area
            events.append({
                'type': 'loitering',
                'person_id': person_id,
                'duration': round(duration, 2),
                'area': round(movement_area, 2),
                'center': (round(sum(xs)/len(xs), 2), round(sum(ys)/len(ys), 2)),
                'severity': 'medium',
                'timestamp': current_time
            })
    
    return events


def draw_activity_overlay(frame: np.ndarray, tracker: PersonTracker, 
                          events: List[Dict]) -> np.ndarray:
    """
    Draw visual indicators for detected abnormal activities.
    
    Args:
        frame: Video frame
        tracker: PersonTracker instance
        events: List of activity events
    
    Returns:
        Frame with activity overlays
    """
    for event in events:
        if event['type'] == 'sudden_movement':
            person_id = event['person_id']
            if person_id in tracker.tracks and len(tracker.tracks[person_id]) > 0:
                pos = tracker.tracks[person_id][-1]['position']
                bbox = tracker.tracks[person_id][-1]['bbox']
                
                # Draw red box around person
                cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), 
                            (int(bbox[2]), int(bbox[3])), (0, 0, 255), 3)
                
                # Draw velocity arrow
                velocity = event['velocity']
                arrow_end = (int(pos[0] + velocity[0] * 0.5), 
                           int(pos[1] + velocity[1] * 0.5))
                cv2.arrowedLine(frame, (int(pos[0]), int(pos[1])), arrow_end, 
                              (0, 0, 255), 2, tipLength=0.3)
                
                # Label
                cv2.putText(frame, f"SUDDEN MOVE {event['speed']:.0f}px/s", 
                          (int(bbox[0]), int(bbox[1]) - 10), 
                          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        
        elif event['type'] == 'crowd_rush':
            # Draw warning banner
            cv2.rectangle(frame, (10, 10), (400, 60), (0, 0, 255), -1)
            cv2.putText(frame, f"CROWD RUSH DETECTED!", 
                       (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            cv2.putText(frame, f"{event['num_people']} people @ {event['avg_speed']:.0f}px/s", 
                       (20, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        elif event['type'] == 'loitering':
            person_id = event['person_id']
            if person_id in tracker.tracks and len(tracker.tracks[person_id]) > 0:
                bbox = tracker.tracks[person_id][-1]['bbox']
                
                # Draw yellow box
                cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), 
                            (int(bbox[2]), int(bbox[3])), (0, 255, 255), 2)
                
                # Label
                cv2.putText(frame, f"LOITERING {event['duration']:.0f}s", 
                          (int(bbox[0]), int(bbox[1]) - 10), 
                          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
    
    return frame
