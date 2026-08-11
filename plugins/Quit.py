def run():
    quit()

def init(reg, settings, cfg, lang):
    reg.register(
        name=f"{lang.t("global_quit")}", 
        show_in_menu=True,
        run_function=run
    )