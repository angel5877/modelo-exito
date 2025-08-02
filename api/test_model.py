import mlflow
from mlflow.tracking import MlflowClient

mlflow.set_tracking_uri("https://9000aca66145.ngrok-free.app")

client = MlflowClient()

# Cambiar el stage de la versión 1 a Production
client.transition_model_version_stage(
    name="randomforest_model",
    version=1,
    stage="Production",
    archive_existing_versions=True
)