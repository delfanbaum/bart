from bart.config import BART_CONFIG_PATHS, BartConfig, MarkupLanguages


class TestConfig:
    """
    Specific tests for config; actual coverage of this function is sort of
    everywhere (for now?)
    """

    def test_use_global_config(self, test_config):
        """
        It should pull in global config paths. For this we just append a test
        path to the config
        """
        BART_CONFIG_PATHS.append(test_config)
        config = BartConfig()
        assert config.markup == MarkupLanguages.MARKDOWN
        # we have to explicitly clean this up, otherwise it remains in memory
        BART_CONFIG_PATHS.remove(test_config)


