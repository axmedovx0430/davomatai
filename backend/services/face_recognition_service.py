"""
Face Recognition Service using InsightFace
"""
import numpy as np
import cv2
from insightface.app import FaceAnalysis
from typing import Optional, Tuple, List
import os
from config import settings
import logging

logger = logging.getLogger(__name__)


class FaceRecognitionService:
    def __init__(self):
        """Initialize InsightFace model"""
        self.app = None
        self.model_loaded = False
        # Do not load model on init to save memory and startup time
        # self.load_model()
    
    def load_model(self):
        """Load InsightFace model lazily"""
        if self.model_loaded:
            return

        try:
            logger.info(f"Loading InsightFace model: {settings.INSIGHTFACE_MODEL}")
            # Only load detection and recognition models to save memory
            self.app = FaceAnalysis(
                name=settings.INSIGHTFACE_MODEL,
                allowed_modules=['detection', 'recognition'],
                providers=['CPUExecutionProvider']
            )
            self.app.prepare(ctx_id=0, det_size=(320, 320))
            
            # Force garbage collection
            import gc
            gc.collect()
            
            self.model_loaded = True
            logger.info("InsightFace model loaded successfully (Lite mode)")
        except Exception as e:
            logger.error(f"Failed to load InsightFace model: {e}")
            raise
    
    def detect_faces(self, image: np.ndarray) -> List:
        """
        Detect faces in image
        
        Args:
            image: numpy array (BGR format from cv2)
            
        Returns:
            List of detected faces with bounding boxes and embeddings
        """
        if not self.model_loaded:
            self.load_model()
            if not self.model_loaded:
                raise RuntimeError("Face recognition model not loaded")
        
        try:
            faces = self.app.get(image)
            return faces
        except Exception as e:
            logger.error(f"Face detection error: {e}")
            return []
    
    def get_embedding(self, image: np.ndarray) -> Optional[np.ndarray]:
        """
        Extract face embedding from image
        
        Args:
            image: numpy array (BGR format)
            
        Returns:
            512-dimensional embedding vector or None if no face detected
        """
        faces = self.detect_faces(image)
        
        if not faces:
            logger.warning("No face detected in image")
            return None
        
        if len(faces) > 1:
            logger.warning(f"Multiple faces detected ({len(faces)}), using the largest one")
            # Use the face with largest bounding box
            faces = sorted(faces, key=lambda x: (x.bbox[2] - x.bbox[0]) * (x.bbox[3] - x.bbox[1]), reverse=True)
        
        # Get embedding from the first/largest face
        embedding = faces[0].embedding
        
        # Normalize embedding
        embedding = embedding / np.linalg.norm(embedding)
        
        return embedding
    
    def compare_embeddings(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """
        Compare two face embeddings using cosine similarity
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Similarity score (0-1, higher is more similar)
        """
        # Calculate cosine similarity using numpy
        # similarity = dot(a, b) / (norm(a) * norm(b))
        dot_product = np.dot(embedding1, embedding2)
        norm1 = np.linalg.norm(embedding1)
        norm2 = np.linalg.norm(embedding2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
            
        similarity = dot_product / (norm1 * norm2)
        return float(similarity)
    
    def find_best_match(
        self, 
        query_embedding: np.ndarray, 
        database_embeddings: List[Tuple[int, np.ndarray]]
    ) -> Optional[Tuple[int, float]]:
        """
        Find best matching face from database
        
        Args:
            query_embedding: Embedding to match
            database_embeddings: List of (face_id, embedding) tuples
            
        Returns:
            (face_id, confidence) or None if no match above threshold
        """
        if not database_embeddings:
            return None
        
        best_match_id = None
        best_similarity = 0.0
        
        for face_id, db_embedding in database_embeddings:
            similarity = self.compare_embeddings(query_embedding, db_embedding)
            
            if similarity > best_similarity:
                best_similarity = similarity
                best_match_id = face_id
        
        # Check if best match is above threshold
        if best_similarity >= settings.FACE_MATCH_THRESHOLD:
            return (best_match_id, best_similarity)
        
        return None
    
    def crop_face(self, image: np.ndarray, target_size: Tuple[int, int] = (400, 400)) -> Optional[np.ndarray]:
        """
        Detect and crop face from image
        
        Args:
            image: Input image
            target_size: Target size for cropped face
            
        Returns:
            Cropped face image or None
        """
        faces = self.detect_faces(image)
        
        if not faces:
            return None
        
        # Get the largest face
        if len(faces) > 1:
            faces = sorted(faces, key=lambda x: (x.bbox[2] - x.bbox[0]) * (x.bbox[3] - x.bbox[1]), reverse=True)
        
        face = faces[0]
        bbox = face.bbox.astype(int)
        
        # Add padding
        padding = 20
        x1 = max(0, bbox[0] - padding)
        y1 = max(0, bbox[1] - padding)
        x2 = min(image.shape[1], bbox[2] + padding)
        y2 = min(image.shape[0], bbox[3] + padding)
        
        # Crop face
        face_img = image[y1:y2, x1:x2]
        
        # Resize to target size
        face_img = cv2.resize(face_img, target_size)
        
        return face_img
    
    def embedding_to_bytes(self, embedding: np.ndarray) -> bytes:
        """Convert numpy embedding to bytes for database storage"""
        return embedding.tobytes()
    
    def bytes_to_embedding(self, embedding_bytes: bytes) -> np.ndarray:
        """Convert bytes back to numpy embedding"""
        return np.frombuffer(embedding_bytes, dtype=np.float32)


# Global instance
face_recognition_service = FaceRecognitionService()
