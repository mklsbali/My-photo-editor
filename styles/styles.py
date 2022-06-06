title_style = {
    "font_family": "Arial",
    "point_size": 22
}
filter_image_dim = 60


image_container_style = "#image_container {border: 1px solid black;" \
                        "border-width: 3;" \
                        "border-color: #888888}"

main_label2_style = "#main_label2 {border: 1px solid black;" \
                        "border-width: 3;" \
                        "border-color: #888888}"

main_label3_style = "#main_label3 {border: 1px solid black;" \
                        "border-width: 3;" \
                        "border-color: #888888}"
negative_button_style = "background-color: #888888;" \
                        "height: 75px;" \
                        "width: 75px;" \
                        "background-image : url(styles/filter_images/test_photo_neg.png);"

gs_button_style = "background-color: #888888;" \
                        "height: 75px;" \
                        "width: 75px;" \
                        "background-image : url(styles/filter_images/test_photo_gs.png);"

b_w_button_style = "background-color: #888888;" \
                        "height: 75px;" \
                        "width: 75px;" \
                        "background-image : url(styles/filter_images/test_photo_bw.png);"

general_label_text_style = "font-size: 15px"

resize_input_style = "font-size: 15px;" \
                     "width: 30px"


def cp_color(color="#99c1f1"):
    cp_style = "#cp_button {background-color:" + color + ";" \
               "width: 70 px;" \
               "height: 18px}"
    return cp_style


def filter_style(f_image_path):
    f_style = "background-color: #888888;" \
                       "height: 75px;" \
                       "width: 75px;" \
                       "background-image : url({});".format(f_image_path)
    return f_style

