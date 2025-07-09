from pathlib import Path
import json
from config.paths import RAW_ACTIVITIES_DIR, PROCESSED_DIR
from utils.iati_helpers import normalize_activity
from utils import slugify, setup_logger

class MineActionTransformer:
    def __init__(self, input_dir=RAW_ACTIVITIES_DIR, output_dir=PROCESSED_DIR / "normalized"):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.logger = setup_logger("transform_mine_action_activities")
        
    def transform_all(self):
        for publisher_dir in self.input_dir.iterdir():
            if not publisher_dir.is_dir():
                continue

            publisher_slug = slugify(publisher_dir.name)
            output_publisher_dir = self.output_dir / publisher_slug
            output_publisher_dir.mkdir(parents=True, exist_ok=True)

            for file in publisher_dir.glob("*.json"):
                self._process_file(file, output_publisher_dir)
                
    def _process_file(self, file_path, output_publisher_dir):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                activity = json.load(f)
                
            normalized = normalize_activity(activity)
            
            output_file = output_publisher_dir / file_path.name
            with open(output_file, 'w', encoding='utf-8') as out_f:
                json.dump(normalized, out_f, ensure_ascii=False, indent=2)
                
            self.logger.info(f"✅ Normalized: {file_path.name}")
        except Exception as e:
            self.logger.error(f"❌ Failed: {file_path.name} | Error: {e}")

    def run(self):
        self.logger.info("🚀 Starting transformation...")
        self.transform_all()
        self.logger.info(f"✅ Transformation complete. Output saved to: {self.output_dir}")


if __name__ == "__main__":
    transformer = MineActionTransformer()
    transformer.run()
