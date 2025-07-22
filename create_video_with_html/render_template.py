def render_template(template_path, output_path, context):
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    for key, value in context.items():
        if key != "LINES":
            if value is None:
                print(f"⚠️ Biến '{key}' có giá trị None, sẽ thay bằng chuỗi rỗng.")
            template = template.replace(f"{{{{{key}}}}}", str(value or ""))

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(template)
