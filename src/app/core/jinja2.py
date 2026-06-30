from fastapi.templating import Jinja2Templates

TEMPLATES_DIR = "./src/templates"

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
