from pydantic_settings import BaseSettings, SettingsConfigDict


class _Settings(BaseSettings):
    API_PASSWORD: str = "test_password"
    HOST: str = "http://localhost:8000"

    EXPENSES_SPREADSHEET_ID: str = "PLACEHOLDER"
    NEXT_YEAR_EXPENSES_SPREADSHEET_ID: str = "PLACEHOLDER"
    SALARIES_SPREADSHEET_ID: str = "PLACEHOLDER"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


Settings = _Settings()  # type: ignore
