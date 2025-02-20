import sys
import importlib.util
import streamlit.web.cli as stcli


def main():
    app_module = importlib.util.find_spec('perplexity_seo.app').origin
    sys.argv = ["streamlit", "run", app_module]
    sys.exit(stcli.main())


if __name__ == "__main__":
    main()
