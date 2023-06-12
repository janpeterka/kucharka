from markupsafe import Markup


def dropzone(action, default_message="sem přetáhni soubor k uložení", id="dropzone"):
    return Markup(
        f"""
    <form action="{action}"
      class="dropzone"
      id="{id}"
      data-controller="dropzone"
    >
      <div class="dz-message text-center" data-dz-message>
        <span>{default_message}</span>
      </div>
    </form>
    """
    )
