
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Starting InsightFace test")

try:
    from insightface.app import FaceAnalysis
    logger.info("Imported FaceAnalysis")
    
    app = FaceAnalysis(name='buffalo_s', providers=['CPUExecutionProvider'])
    logger.info("Initialized FaceAnalysis")
    
    app.prepare(ctx_id=0, det_size=(320, 320))
    logger.info("Prepared FaceAnalysis")
    
    print("Success!")

except Exception as e:
    logger.error(f"Error: {e}")
    import traceback
    traceback.print_exc()

logger.info("Finished InsightFace test")
