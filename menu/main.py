from nicegui import ui, app
import os

menu_path = os.path.dirname(__file__) 
app.add_static_files('/menu', menu_path)

selected_cards = []
all_cards = {}
iframe_container = None
visible_D2T1_natural = True
visible_D2T2_natural = True
visible_D2T3_natural = True
visible_D3T1_natural = True
visible_D3T2_natural = True
visible_D3T3_natural = True
visible_D1T1_natural = True
visible_D1T2_natural = True
visible_D1T3_natural = True



natural_hour= None
natural_day= None

DEFAULT_IMAGE = "XII/Artificial/C1-pv2.exr"

# Helper functions
def show_selected_images():
    def format_exr(image_name):
        if image_name.startswith('/menu/'):
            image_name = image_name[len('/menu/'):]
        parts = image_name.rsplit('/', 1)
        folder = parts[0]
        file_name = parts[1].rsplit('.', 1)[0]
        folder = folder.replace('+', '%2B')
        return f"XII/{folder}/{file_name}.exr"

    if len(selected_cards) == 0:
        url = f"http://127.0.0.1:3006/index.html?img1={DEFAULT_IMAGE}"
    elif len(selected_cards) == 1:
        img1 = DEFAULT_IMAGE
        img2 = format_exr(selected_cards[0]["image"])
        url = f"http://127.0.0.1:3006/index.html?img1={img1}&img2={img2}"
    else:
        img1 = format_exr(selected_cards[0]["image"])
        img2 = format_exr(selected_cards[1]["image"])
        url = f"http://127.0.0.1:3006/index.html?img1={img1}&img2={img2}"

    return f'''
    <div class="w-full h-full">
        <iframe 
            src="{url}" 
            style="width:100%; height:100%; border:none;" 
            allowfullscreen
            loading="lazy">
        </iframe>
    </div>
    '''


def update_all_cards_visibility():
    selected_images = [s["image"] for s in selected_cards]
    for image, buttons in all_cards.items():
        for button in buttons:
            button.set_visibility(image in selected_images)

def card(image, text, classes, max_selected=2):
    with ui.card().tight().classes(classes) as c:
        with ui.image(image) as img:
            button = ui.button(icon='check_circle').props('flat fab color=white').classes('absolute top-0 right-0 m-1')
            button.set_visibility(False)

            if image not in all_cards:
                all_cards[image] = []
            all_cards[image].append(button)

            def toggle_selection():
                global selected_cards, iframe_container
                found = next((s for s in selected_cards if s["image"] == image), None)
                if found:
                    selected_cards = [s for s in selected_cards if s["image"] != image]
                else:
                    if len(selected_cards) >= max_selected:
                        ui.notify(f'⚠️ Only {max_selected} images allowed', color='red')
                        return
                    selected_cards.append({"card": c, "image": image, "text": text})

                update_all_cards_visibility()

                
                if iframe_container:
                    iframe_container.content = show_selected_images()



            img.on('click', toggle_selection)

        with ui.card_section():
            if isinstance(text, list):
                for t in text:
                    ui.markdown(t)
            else:
                ui.markdown(text)


# Category data
NATURAL = "**Natural illumination**: "
NAT_NONE = "**Natural illumination**: no"
ARTIFICIAL = "**Artificial illumination**: "
ART_NONE = "**Artificial illumination**: no"
C1 = "Hanging oil lamp"
C2 = "Two table candles"
C3 = "Two floor chandeliers"
C4 = "Four floor chandeliers"

D1 = "Dec 25th"
D2 = "Apr 1st"
D3 = "Jun 6th"
DD1 = f"Date: {D1}"
DD2 = f"Date: {D2}"   
DD3 = f"Date: {D3}"
D1T1 = "Time: 10:00 am"
D1T2 = "Time: 10:53 am"
D1T3 = "Time: 12:53 pm"
D2T1 = "Time: 10:00 am"
D2T2 = "Time: 10:56 am"
D2T3 = "Time: 13:56 pm"
D3T1 = "Time: 10:00 am"
D3T2 = "Time: 11:53 am"
D3T3 = "Time: 13:53 pm"

@ui.page('/')
def main():
    global iframe_container
    selected_cards.clear()

    categories = ["Inici", "Natural illumination", "Artificial illumination", "Natural + Artificial illumination", "All combinations"]
    menu_panels = {}

    

    ui.add_head_html('''
<style>
body, html {
    margin: 0;
    padding: 0;
    overflow-x: hidden;
}

.menu-row {
    width: 100%;
    margin: 0;
    padding: 0;
    display: flex;
    justify-content: center;
    background-color: white;
}

.dropdown-panel {
    position: absolute;
    top: 50px;
    left: 0;
    right: 0;
    height: 33vh;
    background-color: white;
    overflow-x: auto;
    overflow-y: hidden;
    z-index: 50;
    display: flex;
    justify-content: center;
    align-items: center;
}

/* Fixed size for all cards */
.dropdown-panel .q-card {
    transform: scale(0.65); 
    margin: -30px;         
    display: flex;
    flex-direction: column;
    vertical-align: top;
}
        

/* First thistle with more space on the left */
.dropdown-panel .q-card:first-child {
    margin-left: 20px;
}

/* Set the size of the image inside the card */
.dropdown-panel .q-card .q-img {
    width: 100%;       
    height: 180px;     
    object-fit: cover; 
}

/* Compact text below */
.dropdown-panel .q-card__section {
    
    font-size: 1rem;
    line-height: 1rem;
    text-align: center;
    justify-content:center;
    
}


                    
</style>
''')




   # RESPONSIVE TOP MENU 
    with ui.row().classes('menu-row overflow-x-auto no-scrollbar flex-nowrap').style('white-space: nowrap; justify-content: center; gap: 1rem; padding: 0 20px;'):
        active_panel = {'name': None}

        def show_panel(e, cat):
            # hide all panels
            for name, p in menu_panels.items():
                p.set_visibility(False)
            # show only what is relevant
            if cat != "Inici":
                menu_panels[cat].set_visibility(True)
                active_panel['name'] = cat

        for cat in categories:
            ui.label(cat)\
                .classes('cursor-pointer px-3 py-2 rounded hover:bg-gray-100 transition flex-shrink-0')\
                .on('mouseover', lambda e, cat=cat: show_panel(e, cat))


    # FOLDABLE PANEL
    for cat in categories:
        with ui.column().classes('dropdown-panel') as panel:
            panel.set_visibility(False)
            menu_panels[cat] = panel

            # When it leaves the panel, we hide it
            panel.on('mouseleave', lambda e, cat=cat: menu_panels[cat].set_visibility(False))



   # Function to refresh Natural illumination cards 
    def refresh_cards_natural():
        
       #  We delete old content
        cards_container_natural1.clear()
        cards_container_natural2.clear()
        cards_container_natural3.clear()

       #  Update visibility based on time
        if natural_hour == "10:00":
            visible_D2T1_natural = True
            visible_D2T2_natural = False
            visible_D2T3_natural = False
            visible_D3T1_natural = True
            visible_D3T2_natural = False
            visible_D3T3_natural = False
            visible_D1T1_natural = True
            visible_D1T2_natural = False
            visible_D1T3_natural = False
        elif natural_hour == "10:53":
            visible_D2T1_natural = False
            visible_D2T2_natural = False
            visible_D2T3_natural = False
            visible_D3T1_natural = False
            visible_D3T2_natural = False
            visible_D3T3_natural = False
            visible_D1T1_natural = False
            visible_D1T2_natural = True
            visible_D1T3_natural = False
        elif natural_hour == "10:56":
            visible_D2T1_natural = False
            visible_D2T2_natural = True
            visible_D2T3_natural = False
            visible_D3T1_natural = False
            visible_D3T2_natural = False
            visible_D3T3_natural = False
            visible_D1T1_natural = False
            visible_D1T2_natural = False
            visible_D1T3_natural = False
        elif natural_hour == "11:53":
            visible_D2T1_natural = False
            visible_D2T2_natural = False
            visible_D2T3_natural = False
            visible_D3T1_natural = False
            visible_D3T2_natural = True
            visible_D3T3_natural = False
            visible_D1T1_natural = False
            visible_D1T2_natural = False
            visible_D1T3_natural = False
        elif natural_hour == "12:53":
            visible_D2T1_natural = False
            visible_D2T2_natural = False
            visible_D2T3_natural = False
            visible_D3T1_natural = False
            visible_D3T2_natural = False
            visible_D3T3_natural = False
            visible_D1T1_natural = False
            visible_D1T2_natural = False
            visible_D1T3_natural = True
        elif natural_hour == "13:53":
            visible_D2T1_natural = False
            visible_D2T2_natural = False
            visible_D2T3_natural = False
            visible_D3T1_natural = False
            visible_D3T2_natural = False
            visible_D3T3_natural = True
            visible_D1T1_natural = False
            visible_D1T2_natural = False
            visible_D1T3_natural = False
        elif natural_hour == "13:56":
            visible_D2T1_natural = False
            visible_D2T2_natural = False
            visible_D2T3_natural = True
            visible_D3T1_natural = False
            visible_D3T2_natural = False
            visible_D3T3_natural = False
            visible_D1T1_natural = False
            visible_D1T2_natural = False
            visible_D1T3_natural = False
        else:
            visible_D2T1_natural = True
            visible_D2T2_natural = True
            visible_D2T3_natural = True
            visible_D3T1_natural = True
            visible_D3T2_natural = True
            visible_D3T3_natural = True
            visible_D1T1_natural = True
            visible_D1T2_natural = True
            visible_D1T3_natural = True


       # First column: Apr 1st
        if (visible_D2T1_natural or visible_D2T2_natural or visible_D2T3_natural) and \
        (natural_day is None or natural_day == "Apr 1st" or natural_day == "All"):
            with cards_container_natural1:
                ui.label("Apr 1st").classes('text-sm').style('margin-bottom: 5px; line-height: 1;')
                with ui.row().classes('gap-2 items-start').style('margin-top: -18px; margin-left: -55px;'):
                    if visible_D2T1_natural:
                        card("/menu/natural/D2T1-pv2.jpg", [D2T1], classes)
                    if visible_D2T2_natural:
                        card("/menu/natural/D2T2-pv2.jpg", [D2T2], classes)
                    if visible_D2T3_natural:
                        card("/menu/natural/D2T3-pv2.jpg", [D2T3], classes)


        # Second column: Jun 6th 
        if (visible_D3T1_natural or visible_D3T2_natural or visible_D3T3_natural) and \
        (natural_day is None or natural_day == "Jun 6th" or natural_day == "All"):
            with cards_container_natural2:
                ui.label("Jun 6th").classes('text-sm').style('margin-bottom: 5px; line-height: 1;')
                with ui.row().classes('gap-2 items-start').style('margin-top: -18px; margin-left: -55px;'):
                    if visible_D3T1_natural:
                        card("/menu/natural/D3T1-pv2.jpg", [D3T1], classes)
                    if visible_D3T2_natural:
                        card("/menu/natural/D3T2-pv2.jpg", [D3T2], classes)
                    if visible_D3T3_natural:
                        card("/menu/natural/D3T3-pv2.jpg", [D3T3], classes)

       # Third column: Dec 25th 
        if (visible_D1T1_natural or visible_D1T2_natural or visible_D1T3_natural)and \
        (natural_day is None or natural_day == "Dec 25th" or natural_day == "All"):
            with cards_container_natural3:
                ui.label("Dec 25th").classes('text-sm').style('margin-bottom: 5px; line-height: 1;')
                with ui.row().classes('gap-2 items-start').style('margin-top: -18px; margin-left: -55px;'):
                    if visible_D1T1_natural:
                        card("/menu/natural/D1T1-pv2.jpg", [D1T1], classes)
                    if visible_D1T2_natural:
                        card("/menu/natural/D1T2-pv2.jpg", [D1T2], classes)
                    if visible_D1T3_natural:
                        card("/menu/natural/D1T3-pv2.jpg", [D1T3], classes)

    
        update_all_cards_visibility()


   
    # Natural illumination
    with menu_panels["Natural illumination"]:
        classes = "w-[180px]"

        # main container
        with ui.row().classes('w-full justify-end items-center gap-6').style('padding: 0 40px; margin-top:-16px;'):
            # Relative container for the "Time" menu
            with ui.element('div').classes('relative'):
                label_hour = ui.label("Hour").classes(
                    'text-sm text-gray-500 cursor-pointer hover:text-black select-none'
                )

                # Time selection menu
                with ui.menu().props(
                    'auto-close="false" anchor="bottom middle" self="top middle"'
                ).classes('bg-white shadow-md rounded-md p-2 z-50 w-40') as hour_menu:
                    ui.label("Selecciona hora").classes('text-sm text-gray-600 px-2 py-1')
                    ui.separator()

                    def set_hour(hour):
                        global natural_hour
                        natural_hour = hour
                        refresh_cards_natural()

                    ui.menu_item("All", lambda: set_hour("All"))
                    ui.menu_item("10:00 am", lambda: set_hour("10:00"))
                    ui.menu_item("10:53 am", lambda: set_hour("10:53"))
                    ui.menu_item("10:56 am", lambda: set_hour("10:56"))
                    ui.menu_item("11:53 am", lambda: set_hour("11:53"))
                    ui.menu_item("12:53 pm", lambda: set_hour("12:53"))
                    ui.menu_item("13:53 pm", lambda: set_hour("13:53"))
                    ui.menu_item("13:56 pm", lambda: set_hour("13:56"))

                label_hour.on('click', hour_menu.toggle)

           # Relative container for the "Day" menu
            with ui.element('div').classes('relative'):
                label_day = ui.label("Day").classes(
                    'text-sm text-gray-500 cursor-pointer hover:text-black select-none'
                )

               # Day selection menu
                with ui.menu().props(
                    'auto-close="false" anchor="bottom middle" self="top middle"'
                ).classes('bg-white shadow-md rounded-md p-2 z-50 w-40') as day_menu:
                    ui.label("Selecciona dia").classes('text-sm text-gray-600 px-2 py-1')
                    ui.separator()

                    def set_day(day):
                        global natural_day
                        natural_day = day
                        refresh_cards_natural()

                    ui.menu_item("All", lambda: set_day("All"))
                    ui.menu_item("Apr 1st", lambda: set_day("Apr 1st"))
                    ui.menu_item("Jun 6th", lambda: set_day("Jun 6th"))
                    ui.menu_item("Dec 25th", lambda: set_day("Dec 25th"))
                    

                label_day.on('click', day_menu.toggle)

          # view label 
            ui.label("View").classes('text-sm text-gray-500')

        #Content with horizontal scroll
        with ui.row().classes('w-full overflow-x-auto no-scrollbar').style('padding-left: 40px; white-space: nowrap; padding-top: 0px;'):
            with ui.row().classes('justify-start gap-8 items-start flex-nowrap').style('display: inline-flex;'):
                # First column: Apr 1st
                with ui.column().classes('items-start flex-shrink-0').style('align-items: flex-start; margin-left: 0px;') as cards_container_natural1:
                    pass

                # Second column: Jun 6th
                with ui.column().classes('items-start flex-shrink-0').style('align-items: flex-start; margin-left: 0px;') as cards_container_natural2:
                    pass

                # Third column: Dec 25th
                with ui.column().classes('items-start flex-shrink-0').style('align-items: flex-start; margin-left: 0px;') as cards_container_natural3:
                    pass

        
        refresh_cards_natural()


    # Artificial illumination
    with menu_panels["Artificial illumination"]:
        classes = "w-[180px] h-[295px]"

        with ui.row().classes('w-full justify-end items-center gap-6').style('padding: 0px 40px 0 40px;'):
            ui.label("Hora").classes('text-sm text-gray-500')
            ui.label("Dia").classes('text-sm text-gray-500')
            ui.label("Vista").classes('text-sm text-gray-500')

        with ui.row().classes('w-full overflow-x-auto no-scrollbar').style('padding-left: 40px; white-space: nowrap; padding-top: 0px;'):
            with ui.row().classes('justify-start gap-8 items-start flex-nowrap').style('display: inline-flex;'):
                
                
                with ui.column().classes('items-start flex-shrink-0').style('align-items: flex-start; margin-left: 0px;'):
                    
                    with ui.row().classes('gap-2 items-start').style('margin-top: -18px; margin-left: -55px;'):

                        card("/menu/artificial/C1-pv2.jpg", [C1], classes)
                        card("/menu/artificial/C2-pv2.jpg", [C2], classes)
                        card("/menu/artificial/C3-pv2.jpg", [C3], classes)
                        card("/menu/artificial/C4-pv2.jpg", [C4], classes)
                        card("/menu/artificial/C5-pv2.jpg", [C1, C2, C4], classes)


  

    # Natural + Artificial illumination
    with menu_panels["Natural + Artificial illumination"]:
        classes = "w-[180px] h-[320px]"
        scale = "transform: scale(0.85); transform-origin: top center; transition: transform 0.3s ease;"

        with ui.row().classes('w-full justify-end items-center gap-6').style('padding: 0px 40px 0 40px; margin-top:5px'):
            ui.label("Hora").classes('text-sm text-gray-500')
            ui.label("Dia").classes('text-sm text-gray-500')
            ui.label("Vista").classes('text-sm text-gray-500')

        


       #Container with horizontal scroll if they don't all fit
        with ui.row().classes('w-full overflow-x-auto no-scrollbar').style('padding-left: 40px; white-space: nowrap; padding-top: 0px;'):
            with ui.row().classes('justify-start gap-1 items-start flex-nowrap').style('display: inline-flex;'):

                # First column: Apr 1st
                with ui.column().classes('items-start flex-shrink-0').style('align-items: flex-start; margin-left: 0px;'):
                    ui.label("Apr 1st").classes('text-sm').style('margin-bottom: 5px; line-height: 1;')
                    with ui.row().classes('gap-2 items-start').style('margin-top: -18px; margin-left: -45px;transform: scale(0.80); transform-origin: top left;'):
                        card("/menu/Natural+Artificial/D2T3-C2-pv2.jpg", [D2T3,C2], classes)
                        card("/menu/Natural+Artificial/D2T3-C5-pv2.jpg", [D2T3,C1,C2,C4], classes)
            
                # Third column: Dec 25th
                with ui.column().classes('items-start flex-shrink-0').style('align-items: flex-start; margin-left: -30px;'):
                    ui.label("Dec 25th").classes('text-sm').style('margin-bottom: 5px; line-height: 1;')
                    with ui.row().classes('gap-2 items-start').style('margin-top: -18px; margin-left: -45px;transform: scale(0.80); transform-origin: top left;'):
                        card("/menu/Natural+Artificial/D1T3-C2-pv2.jpg", [D1T3,C2], classes)
                        card("/menu/Natural+Artificial/D1T3-C5-pv2.jpg", [D1T3,C1,C2,C4], classes)

    
    #All Combinations
    with menu_panels["All combinations"]:
        classes = "w-[180px]"

        with ui.row().classes('w-full justify-end items-center gap-6').style('padding: 0px 40px 0 40px; margin-top:5px'):
            ui.label("Hora").classes('text-sm text-gray-500')
            ui.label("Dia").classes('text-sm text-gray-500')
            ui.label("Vista").classes('text-sm text-gray-500')

        #Container with horizontal scroll
        with ui.row().classes('w-full overflow-x-auto no-scrollbar').style('padding-left: 40px; white-space: nowrap; padding-top: 0px;'):
            with ui.row().classes('justify-start gap-16 items-start flex-nowrap').style('display: inline-flex;'):

                #Natural
                with ui.column().classes('items-start flex-shrink-0').style('align-items: flex-start;'):
                    ui.label("Natural illumination").classes('text-black text-sm font-semibold').style('margin-bottom: 10px;')

                    with ui.row().classes('justify-start gap-1 items-start flex-nowrap').style('display: inline-flex;'):

                        # First column: Apr 1st
                        with ui.column().classes('items-start flex-shrink-0'):
                            ui.label("Apr 1st").classes('text-sm').style('margin-bottom: 5px;')
                            with ui.row().classes('gap-2 items-start').style('margin-top: -18px; margin-left: -45px; transform: scale(0.80); transform-origin: top left;'):
                                card("/menu/natural/D2T1-pv2.jpg", [D2T1], classes)
                                card("/menu/natural/D2T2-pv2.jpg", [D2T2], classes)
                                card("/menu/natural/D2T3-pv2.jpg", [D2T3], classes)

                        # Second column: Jun 6th
                        with ui.column().classes('items-start flex-shrink-0').style('margin-left: -55px;'):
                            ui.label("Jun 6th").classes('text-sm').style('margin-bottom: 5px;')
                            with ui.row().classes('gap-2 items-start').style('margin-top: -18px; margin-left: -45px; transform: scale(0.80); transform-origin: top left;'):
                                card("/menu/natural/D3T1-pv2.jpg", [D3T1], classes)
                                card("/menu/natural/D3T2-pv2.jpg", [D3T2], classes)
                                card("/menu/natural/D3T3-pv2.jpg", [D3T3], classes)

                        # Third column: Dec 25th
                        with ui.column().classes('items-start flex-shrink-0').style('margin-left: -55px;'):
                            ui.label("Dec 25th").classes('text-sm').style('margin-bottom: 5px;')
                            with ui.row().classes('gap-2 items-start').style('margin-top: -18px; margin-left: -45px; transform: scale(0.80); transform-origin: top left;'):
                                card("/menu/natural/D1T1-pv2.jpg", [D1T1], classes)
                                card("/menu/natural/D1T2-pv2.jpg", [D1T2], classes)
                                card("/menu/natural/D1T3-pv2.jpg", [D1T3], classes)


                #Artificial
                with ui.column().classes('items-start flex-shrink-0').style('align-items: flex-start; margin-left:-110px'):
                    ui.label("Artificial illumination").classes('text-black text-sm font-semibold').style('margin-bottom: 10px;')

                    with ui.row().classes('gap-2 items-start').style('margin-left: -40px; margin-top: -10px; transform: scale(0.80); transform-origin: top left;'):
                        card("/menu/artificial/C1-pv2.jpg", [C1], "h-[295px] w-[180px]")
                        card("/menu/artificial/C2-pv2.jpg", [C2], "h-[295px] w-[180px]")
                        card("/menu/artificial/C3-pv2.jpg", [C3], "h-[295px] w-[180px]")
                        card("/menu/artificial/C4-pv2.jpg", [C4], "h-[295px] w-[180px]")
                        card("/menu/artificial/C5-pv2.jpg", [C1, C2, C4], "h-[295px] w-[180px]")

                
                #Natural + Artificial
                with ui.column().classes('items-start flex-shrink-0').style('align-items: flex-start; margin-left:-150px'):
                    ui.label("Natural + Artificial illumination").classes('text-black text-sm font-semibold').style('margin-bottom: 10px;')

                    with ui.row().classes('justify-start gap-1 items-start flex-nowrap').style('display: inline-flex;'):
                        
                        #  First column: Apr 1st
                        with ui.column().classes('items-start flex-shrink-0').style('margin-left: 0px;'):
                            ui.label("Apr 1st").classes('text-sm').style('margin-bottom: 5px;')
                            with ui.row().classes('gap-2 items-start').style('margin-top: -18px; margin-left: -35px; transform: scale(0.59); transform-origin: top left;'):
                                card("/menu/Natural+Artificial/D2T3-C2-pv2.jpg", [D2T3, C2], "w-[180px] h-[320px]")
                                card("/menu/Natural+Artificial/D2T3-C5-pv2.jpg", [D2T3, C1, C2, C4], "w-[180px] h-[320px]")

                        # Second column: Dec 25th
                        with ui.column().classes('items-start flex-shrink-0').style('margin-left: -90px;'):
                            ui.label("Dec 25th").classes('text-sm').style('margin-bottom: 5px;')
                            with ui.row().classes('gap-2 items-start').style('margin-top: -18px; margin-left: -35px; transform: scale(0.59); transform-origin: top left;'):
                                card("/menu/Natural+Artificial/D1T3-C2-pv2.jpg", [D1T3, C2], "w-[180px] h-[320px]")
                                card("/menu/Natural+Artificial/D1T3-C5-pv2.jpg", [D1T3, C1, C2, C4], "w-[180px] h-[320px]")



            


    # Main viewer occupying all the rest of the screen
    iframe_container = ui.html(show_selected_images(), sanitize=False)\
    .classes('w-screen')\
    .style('height: calc(100vh - 50px); position: relative; z-index: 0; margin-left: -16px;')




    # Hide panels only when we stop hovering over the panel
    for panel in menu_panels.values():
        panel.on('mouseleave', lambda e, p=panel: p.set_visibility(False))

ui.run()
