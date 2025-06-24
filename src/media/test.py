import easyocr
import time


def extract_text_from_image(image_path):
    # Create an EasyOCR Reader instance (no GPU)
    reader = easyocr.Reader(['en'], gpu=False)

    # Start timing
    start_time = time.time()

    # Read text from image
    results = reader.readtext(image_path)

    # End timing
    end_time = time.time()
    duration = end_time - start_time

    # Print extracted text
    print("Detected Text:")
    for bbox, text, confidence in results:
        print(f"• {text} (Confidence: {confidence:.2f})")

    # Print duration
    print(f"\nText extraction duration: {duration:.2f} seconds")

if __name__ == "__main__":
    extract_text_from_image(r"C:\Users\andre\Documents\Analysis - IRI\BSA 0.12mg ready\Image819.jpg")