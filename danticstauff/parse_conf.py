from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)




class ImadSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file="app.dev.conf",env_file_encoding='utf-8',env_prefix="IMAD_",extra="ignore")

    app_name:str
    environment:str
    app_version:str


    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (dotenv_settings,)



settings = ImadSettings()
print(settings.model_dump())
