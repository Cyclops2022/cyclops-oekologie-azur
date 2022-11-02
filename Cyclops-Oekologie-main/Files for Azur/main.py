# Pakete importieren
import pandas as pd
import numpy as np
import dash
from dash import Dash, dcc, html, Input, Output  # , State
import plotly.express as px
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

#  import time

######################  Read Data  #####################################

df = pd.read_csv("Emissionen_von_Recyclingprozessen.csv")
# Behebe Einlesefehler
df = df.iloc[:293]
df = df.drop(columns=df.columns[-3:], axis=1)
# Fülle empty values in Beschreibung und Kunststoffe mit "-"
df["Beschreibung"] = df["Beschreibung"].fillna('-')
df["Kunststoffe"] = df["Kunststoffe"].fillna('-')
# Filter Zeilen, die keine Informationen enthalten, d.h. in denen weder leistung noch Durchsatz angegeben sind
df = df.loc[np.invert(np.isnan(df["Leistung"])) | np.invert(np.isnan(df["Durchsatzleistung"]))]

###################### Build Dashboard ##################################

wi_colors = ["#006D72", "#4191AD", "#83B0B6", "#3A89A4", "#AB0026", "#999999", "#E40033"]

speicher_emissionsmatrix = np.zeros((12, 12))

oekostromfaktor = 1  # Wird entsprechend angepasst, wenn Ökostrom verwendet wird

# Zwischenspeichern der Daten, damit diese automatisch wieder angezeigt werden
a = list(range(12)) * 12
t = [[i] * 12 for i in range(12)]
b = []
for i in range(12):
    b = b + t[i]
storage = pd.DataFrame({"i": a, "j": b})
storage["Auswahl"] = np.nan
storage["Leistung"] = np.nan
storage["Durchsatz"] = np.nan

indizes = np.zeros(2)

kategorien = ["Öffnen, Auflösen", "Zerkleinern", 'Trennen', 'Waschen', 'Trocknen', 'Agglomerieren, Verdichten',
              'Kombinierte Anlagen']
tab_labels = ["Öffnen, Auflösen", "Zerkleinern", 'Trennen', 'Waschen', 'Trocknen', 'Agglomerieren, Verdichten',
              'Kombinierte Anlagen']

# Baue das Dashboard
dash_app = Dash(external_stylesheets=[dbc.themes.FLATLY], suppress_callback_exceptions=True)
app = dash_app.server

tabs_styles = {
    'height': '75px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '12px',
    'fontWeight': 'bold',
    'display': 'flex',
    'align-items': 'center',
    'justify-content': 'center'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#83B0B6',
    'fontWeight': 'bold',
    'color': 'white',
    'padding': '12px',
    'display': 'flex',
    'align-items': 'center',
    'justify-content': 'center'
}

subtab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '12px',
    'fontWeight': 'bold',
    'width': '250px',
    'height': '100px',
    'display': 'flex',
    'align-items': 'center'
}

subtab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#83B0B6',
    'color': 'white',
    'fontWeight': 'bold',
    'padding': '12px',
    'display': 'flex',
    'align-items': 'center'
}

dash_app.layout = html.Div([
    html.Br(),
    html.H1("Emissionen von Recyclingprozessen", style={'text-align': 'center', 'color': '#006D72'}),
    html.Br(),
    html.Div([dcc.Markdown('''
#### Dieses Dashboard gibt Ihnen eine Übersicht über die Treibhausgasemissionen des von Ihnen verwendeten Aufbereitungsverfahrens.    
Im ersten Schritt geben Sie die von Ihnen verwendeten Verfahrensschritte an.
Die Berechnung der Emissionen erfolgt auf Grundlage des Stromverbrauchs und des Durchsatzes der Anlagen.
Für einige Maschinen stehen die Daten zu Leistungsaufnahme und Durchsatz aus unserer Datenbank zur Verfügung.
Diese können Sie für den jeweiligen Prozessschritt auswählen. Falls die Daten nicht vorhanden sind,
können Sie die entsprechenden Informationen selber eintragen. 

Bitte speichern Sie die Angaben mit einem Klick auf den Button "Angaben speichern" und tragen Sie dann die Angaben für alle weiteren Prozessschritte ein. 
Sie sehen dann im unteren Teil des Dashboards eine Auswertung über die Emissionen aus den verschiedenen Prozessschritten.

Die Daten hier geben dabei nur eine Übersicht über die Emissionen die aus dem Stromverbrauch der Anlagen entstehen. 
Andere Emissionen werden dabei vernachlässigt. 
Das können z.B. Emissionen für die Bereitstellung von Betriebsmitteln wie Waschwasser sein, Emissionen für Transport und
 Logistik von und zu Ihrem Unternehmen aber auch innerhalb Ihres Prozesses, oder Emissionen die durch die Bereitstellung
  der Infrastruktur und Anlagen entstehen. Um eine vollständige Übersicht über all diese Emissionen zu erhalten,
   empfehlen wir Ihnen sich mit unseren Kollegen vom [SKZ](mailto:h.achenbach@skz.de) in Verbindung zu setzen.

Das Dashboard entstand im Rahmen des CYCLOPS Projektes, gefördert durch das Bundesministerium für Bildung und Forschung.'''),]),
    html.Br(),

    # html.H4("Angaben zur Stromversorgung"),
    # html.Br(),
    # dcc.Checklist(options=["Ökostrom", "Konventioneller Strom"], value=["Konventioneller Strom"],
    # id="Ökostrom", labelStyle={'fontSize': '18px'}, style={'display': 'flex', 'marginLeft':'5%'}),
    html.Br(),
    html.H4("Bitte die Angaben zum Recyclingprozess ausfüllen"),

    dcc.Tabs(id="Überkategorien", value='Öffnen, Auflösen', children=[
        dcc.Tab(label='Öffnen und Dosieren', value='Öffnen, Auflösen', id="tab-öffnen", style=tab_style,
                selected_style=tab_selected_style),
        dcc.Tab(label='Zerkleinern', value='Zerkleinern', id="tab-zerkleinern", style=tab_style,
                selected_style=tab_selected_style),
        dcc.Tab(label='Trennen', value='Trennen', id="tab-trennen", style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Waschen', value='Waschen', id="tab-waschen", style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Trocknen', value='Trocknen', id="tab-trocknen", style=tab_style,
                selected_style=tab_selected_style),
        dcc.Tab(label='Agglomerieren, Verdichten', value='Agglomerieren, Verdichten', id="tab-verdichten",
                style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Kombinierte Anlagen', value='Kombinierte Anlagen', id="tab-kombinierte", style=tab_style,
                selected_style=tab_selected_style),

    ], style=tabs_styles),
    html.Div(id='tabs'),  # Hier kommt das jeweilige Fenster des Prozessschrittes rein

    dcc.Store(id="Speicher_Indizes"),
    dcc.Store(id="Speicher_Emissionsmatrix", data=speicher_emissionsmatrix),
    dcc.Store(id="Zwischenspeicher", data=speicher_emissionsmatrix),
    dcc.Store(id="Speicher_Auswahl", data=storage.to_json()),
    dcc.Store(id="Zwischenspeicher_Auswahl", data=storage.to_json()),

    html.Br(),
    html.Button("Ergebnisse anzeigen", id="Button-Ergebnisse", n_clicks=0),
    html.Br(),
    html.Div(id="Gesamtemissionen", style={'backgroundColor': "#E6EFF0"}),
    html.Br(),
    dbc.Row([dcc.Graph(id="Ergebnisgrafik", figure={})], style={'marginLeft': '10%', 'width': '80%'}),
    html.Br(),
    html.Div([html.Button("Download Excel", id="btn_csv"),
              dcc.Download(id="download-dataframe-csv"), ]),
    html.Br(),
    html.Br(),
    html.Div([dcc.Markdown('''
#### Impressum:        
Kontakt: Phillip Bendix, Wuppertal Institut - [phillip.bendix@wupperinst.org](mailto:phillip.bendix@wupperinst.org)   
Umsetzung: Jonathan Kirchhoff, Maike Jansen, Phillip Bendix'''), ])

])


@dash_app.callback(
    Output('tabs', 'children'),
    Input('Überkategorien', 'value'), prevent_initial_callback=True
)
def cb_tabs_rendern(ueberkat):
    if ueberkat == "Öffnen, Auflösen":
        indizes[0] = 0

        return html.Div([
            dbc.Row([
                html.Div(children=[  # Überschrift und Tabs mit Unterkategorien links
                    html.Br(),
                    html.H4("Prozessschritte auswählen"),
                    html.Br()], style={'marginLeft': '10%', 'width': '100%'}
                )
            ]),
            dbc.Row([
                dbc.Col([
                    html.Div(children=[  # Tabs mit Unterkategorien links

                        dcc.Tabs(id="Unterkategorien", vertical=True,
                                 value=list(set(df["Unter-Kategorie"].loc[df["Über-Kategorie"] == ueberkat]))[0],
                                 children=[dcc.Tab(
                                     label=list(set(df["Unter-Kategorie"].loc[df["Über-Kategorie"] == ueberkat]))[i],
                                     value=list(set(df["Unter-Kategorie"].loc[df["Über-Kategorie"] == ueberkat]))[i],
                                     style=subtab_style, selected_style=subtab_selected_style) for i in range(
                                     len(list(set(df["Unter-Kategorie"].loc[df["Über-Kategorie"] == ueberkat]))))],
                                 style=tabs_styles),

                        html.Br()

                    ]),
                ], style={'marginLeft': '0%'}, width=3),
                dbc.Col([
                    dbc.Row(html.Div(id="Auswahl-Unterkat", children=[], style={'width': '100%'})),
                    html.Br(),
                    dbc.Row(html.Div(id="Geräteemissionen", children=["Emissionen: "],
                                     style={'width': '100%', 'backgroundColor': "#E6EFF0"})),
                    # 'backgroundColor': "#E6EFF0"})
                    html.Br(),
                    html.Button("Angaben speichern", id="Übernehmen", n_clicks=0),
                    html.Button("Angaben löschen", id="Löschen", n_clicks=0)
                ], style={'marginRight': '0%'}, width=True)
            ], style={'marginLeft': '10%', 'width': '80%', 'height': '40vh'})

        ]),

    if ueberkat == "Zerkleinern":
        indizes[0] = 1

        return html.Div([
            dbc.Row([
                html.Div(children=[  # Überschrift und Tabs mit Unterkategorien links
                    html.Br(),
                    html.H4("Prozessschritte auswählen"),
                    html.Br()], style={'marginLeft': '10%', 'width': '50%'}
                )
            ]),
            dbc.Row([
                dbc.Col([
                    html.Div(children=[  # Tabs mit Unterkategorien links

                        dcc.Tabs(id="Unterkategorien", vertical=True,
                                 value=list(set(df["Unter-Kategorie"].loc[df["Über-Kategorie"] == ueberkat]))[0],
                                 children=[dcc.Tab(
                                     label=list(set(df["Unter-Kategorie"].loc[df["Über-Kategorie"] == ueberkat]))[i],
                                     value=list(set(df["Unter-Kategorie"].loc[df["Über-Kategorie"] == ueberkat]))[i],
                                     style=subtab_style, selected_style=subtab_selected_style) for i in range(
                                     len(list(set(df["Unter-Kategorie"].loc[df["Über-Kategorie"] == ueberkat]))))],
                                 style=tabs_styles),

                        html.Br()

                    ]),
                ], style={'marginLeft': '0%'}, width=3),
                dbc.Col([
                    dbc.Row(html.Div(id="Auswahl-Unterkat", children=[], style={'width': '120%'})),
                    html.Br(),
                    dbc.Row(html.Div(id="Geräteemissionen", children=["Emissionen: "],
                                     style={'width': '120%', 'backgroundColor': "#E6EFF0"})),
                    # 'backgroundColor': "#E6EFF0"})
                    html.Br(),
                    html.Button("Angaben speichern", id="Übernehmen", n_clicks=0),
                    html.Button("Angaben löschen", id="Löschen", n_clicks=0)
                ], style={'marginRight': '0%'}, width=True)
            ], style={'marginLeft': '10%', 'width': '80%', 'height': '70vh'})

        ]),

    if ueberkat == "Trennen":
        indizes[0] = 2

        return html.Div([
            dbc.Row([
                html.Div(children=[  # Überschrift und Tabs mit Unterkategorien links
                    html.Br(),
                    html.H4("Prozessschritte auswählen"),
                    html.Br()], style={'marginLeft': '10%', 'width': '50%'}
                )
            ]),
            dbc.Row([
                dbc.Col([
                    html.Div(children=[  # Tabs mit Unterkategorien links

                        dcc.Tabs(id="Unterkategorien", vertical=True,
                                 value=list(set(df["Unter-Kategorie"].loc[df["Über-Kategorie"] == ueberkat]))[0],
                                 children=[dcc.Tab(
                                     label=list(set(df["Unter-Kategorie"].loc[df["Über-Kategorie"] == ueberkat]))[i],
                                     value=list(set(df["Unter-Kategorie"].loc[df["Über-Kategorie"] == ueberkat]))[i],
                                     style=subtab_style, selected_style=subtab_selected_style) for i in range(
                                     len(list(set(df["Unter-Kategorie"].loc[df["Über-Kategorie"] == ueberkat]))))],
                                 style=tabs_styles),

                        html.Br()

                    ]),
                ], style={'marginLeft': '0%'}, width=3),
                dbc.Col([
                    dbc.Row(html.Div(id="Auswahl-Unterkat", children=[], style={'width': '100%'})),
                    html.Br(),
                    dbc.Row(html.Div(id="Geräteemissionen", children=["Emissionen: "],
                                     style={'width': '100%', 'backgroundColor': "#E6EFF0"})),
                    # 'backgroundColor': "#E6EFF0"})
                    html.Br(),
                    html.Button("Angaben speichern", id="Übernehmen", n_clicks=0),
                    html.Button("Angaben löschen", id="Löschen", n_clicks=0)
                ], style={'marginRight': '0%'}, width=True)
            ], style={'marginLeft': '10%', 'width': '80%', 'height': '80vh'})

        ]),

    if ueberkat == "Waschen":
        indizes[0] = 3

        return html.Div([
            dbc.Row([
                html.Div(children=[  # Überschrift und Tabs mit Unterkategorien links
                    html.Br(),
                    html.H4("Prozessschritte auswählen"),
                    html.Br()], style={'marginLeft': '10%', 'width': '80%'}
                )
            ]),
            dbc.Row([
                dbc.Col([
                    html.Div(children=[  # Tabs mit Unterkategorien links

                        dcc.Tabs(id="Unterkategorien", vertical=True,
                                 value=list(set(df["Unter-Kategorie"].loc[df["Über-Kategorie"] == ueberkat]))[0],
                                 children=[dcc.Tab(
                                     label=list(set(df["Unter-Kategorie"].loc[df["Über-Kategorie"] == ueberkat]))[i],
                                     value=list(set(df["Unter-Kategorie"].loc[df["Über-Kategorie"] == ueberkat]))[i],
                                     style=subtab_style, selected_style=subtab_selected_style) for i in range(
                                     len(list(set(df["Unter-Kategorie"].loc[df["Über-Kategorie"] == ueberkat]))))],
                                 style=tabs_styles),

                        html.Br()

                    ]),
                ], style={'marginLeft': '0%'}, width=3),
                dbc.Col([
                    dbc.Row(html.Div(id="Auswahl-Unterkat", children=[], style={'width': '120%'})),
                    html.Br(),
                    dbc.Row(html.Div(id="Geräteemissionen", children=["Emissionen: "],
                                     style={'width': '120%', 'backgroundColor': "#E6EFF0"})),
                    # 'backgroundColor': "#E6EFF0"})
                    html.Br(),
                    html.Button("Angaben speichern", id="Übernehmen", n_clicks=0),
                    html.Button("Angaben löschen", id="Löschen", n_clicks=0)
                ], style={'marginRight': '0%'}, width=True)
            ], style={'marginLeft': '10%', 'width': '80%', 'height': '40vh'})

        ]),

    if ueberkat == "Trocknen":
        indizes[0] = 4

        return html.Div([
            dbc.Row([
                html.Div(children=[  # Überschrift und Tabs mit Unterkategorien links
                    html.Br(),
                    html.H4("Prozessschritte auswählen"),
                    html.Br()], style={'marginLeft': '10%', 'width': '50%'}
                )
            ]),
            dbc.Row([
                dbc.Col([
                    html.Div(children=[  # Tabs mit Unterkategorien links

                        dcc.Tabs(id="Unterkategorien", vertical=True,
                                 value=list(set(df["Unter-Kategorie"].loc[df["Über-Kategorie"] == ueberkat]))[0],
                                 children=[dcc.Tab(
                                     label=list(set(df["Unter-Kategorie"].loc[df["Über-Kategorie"] == ueberkat]))[i],
                                     value=list(set(df["Unter-Kategorie"].loc[df["Über-Kategorie"] == ueberkat]))[i],
                                     style=subtab_style, selected_style=subtab_selected_style) for i in range(
                                     len(list(set(df["Unter-Kategorie"].loc[df["Über-Kategorie"] == ueberkat]))))],
                                 style=tabs_styles),

                        html.Br()

                    ]),
                ], style={'marginLeft': '0%'}, width=3),
                dbc.Col([
                    dbc.Row(html.Div(id="Auswahl-Unterkat", children=[], style={'width': '120%'})),
                    html.Br(),
                    dbc.Row(html.Div(id="Geräteemissionen", children=["Emissionen: "],
                                     style={'width': '120%', 'backgroundColor': "#E6EFF0"})),
                    # 'backgroundColor': "#E6EFF0"})
                    html.Br(),
                    html.Button("Angaben speichern", id="Übernehmen", n_clicks=0),
                    html.Button("Angaben löschen", id="Löschen", n_clicks=0)
                ], style={'marginRight': '0%'}, width=True)
            ], style={'marginLeft': '10%', 'width': '80%', 'height': '40vh'})

        ]),

    if ueberkat == "Agglomerieren, Verdichten":
        indizes[0] = 5

        return html.Div([
            dbc.Row([
                html.Div(children=[  # Überschrift und Tabs mit Unterkategorien links
                    html.Br(),
                    html.H4("Prozessschritte auswählen"),
                    html.Br()], style={'marginLeft': '10%', 'width': '50%'}
                )
            ]),
            dbc.Row([
                dbc.Col([
                    html.Div(children=[  # Tabs mit Unterkategorien links

                        dcc.Tabs(id="Unterkategorien", vertical=True,
                                 value=list(set(df["Unter-Kategorie"].loc[df["Über-Kategorie"] == ueberkat]))[0],
                                 children=[dcc.Tab(
                                     label=list(set(df["Unter-Kategorie"].loc[df["Über-Kategorie"] == ueberkat]))[i],
                                     value=list(set(df["Unter-Kategorie"].loc[df["Über-Kategorie"] == ueberkat]))[i],
                                     style=subtab_style, selected_style=subtab_selected_style) for i in range(
                                     len(list(set(df["Unter-Kategorie"].loc[df["Über-Kategorie"] == ueberkat]))))],
                                 style=tabs_styles),

                        html.Br()

                    ]),
                ], style={'marginLeft': '0%'}, width=3),
                dbc.Col([
                    dbc.Row(html.Div(id="Auswahl-Unterkat", children=[], style={'width': '120%'})),
                    html.Br(),
                    dbc.Row(html.Div(id="Geräteemissionen", children=["Emissionen: "],
                                     style={'width': '120%', 'backgroundColor': "#E6EFF0"})),
                    # 'backgroundColor': "#E6EFF0"})
                    html.Br(),
                    html.Button("Angaben speichern", id="Übernehmen", n_clicks=0),
                    html.Button("Angaben löschen", id="Löschen", n_clicks=0)
                ], style={'marginRight': '0%'}, width=True)
            ], style={'marginLeft': '10%', 'width': '80%', 'height': '40vh'})  # 60vh

        ]),

    if ueberkat == "Kombinierte Anlagen":
        indizes[0] = 6

        return html.Div([
            dbc.Row([
                html.Div(children=[  # Überschrift und Tabs mit Unterkategorien links
                    html.Br(),
                    html.H4("Prozessschritte auswählen"),
                    html.Br()], style={'marginLeft': '10%', 'width': '50%'}
                )
            ]),
            dbc.Row([
                dbc.Col([
                    html.Div(children=[  # Tabs mit Unterkategorien links

                        dcc.Tabs(id="Unterkategorien", vertical=True,
                                 value=list(set(df["Unter-Kategorie"].loc[df["Über-Kategorie"] == ueberkat]))[0],
                                 children=[dcc.Tab(
                                     label=list(set(df["Unter-Kategorie"].loc[df["Über-Kategorie"] == ueberkat]))[i],
                                     value=list(set(df["Unter-Kategorie"].loc[df["Über-Kategorie"] == ueberkat]))[i],
                                     style=subtab_style, selected_style=subtab_selected_style) for i in range(
                                     len(list(set(df["Unter-Kategorie"].loc[df["Über-Kategorie"] == ueberkat]))))],
                                 style=tabs_styles),

                        html.Br()

                    ]),
                ], style={'marginLeft': '0%'}, width=3),
                dbc.Col([
                    dbc.Row(html.Div(id="Auswahl-Unterkat", children=[], style={'width': '120%'})),
                    html.Br(),
                    dbc.Row(html.Div(id="Geräteemissionen", children=["Emissionen: "],
                                     style={'width': '120%', 'backgroundColor': "#E6EFF0"})),
                    # 'backgroundColor': "#E6EFF0"})
                    html.Br(),
                    html.Button("Angaben speichern", id="Übernehmen", n_clicks=0),
                    html.Button("Angaben löschen", id="Löschen", n_clicks=0)
                ], style={'marginRight': '0%'}, width=True)
            ], style={'marginLeft': '10%', 'width': '80%', 'height': '40vh'})

        ]),


@dash_app.callback(
    Output('Auswahl-Unterkat', 'children'), Output('Speicher_Indizes', 'data'),
    Input('Überkategorien', 'value'), Input('Unterkategorien', 'value'), prevent_initial_callback=True
)
def cb_angaben_unterkategorien(ueberkat, unterkat):
    indizes[0] = int(np.where(np.array(kategorien) == ueberkat)[0])
    if len(np.where(np.array(list(set(df["Unter-Kategorie"].loc[df["Über-Kategorie"] == ueberkat]))) == unterkat)[
               0]) > 0:
        indizes[1] = int(
            np.where(np.array(list(set(df["Unter-Kategorie"].loc[df["Über-Kategorie"] == ueberkat]))) == unterkat)[0])
        labels = sorted(list(set(
            [
                "Hersteller: " + df["Hersteller"].loc[
                    (df["Über-Kategorie"] == ueberkat) & (df["Unter-Kategorie"] == unterkat)][i] +
                "   Modell: " + df["Beschreibung"].loc[
                    (df["Über-Kategorie"] == ueberkat) & (df["Unter-Kategorie"] == unterkat)][i] +
                "   Leistung: " + str(
                    df["Leistung"].loc[(df["Über-Kategorie"] == ueberkat) & (df["Unter-Kategorie"] == unterkat)][i]) +
                " kW" + " Material: " +
                df["Kunststoffe"].loc[(df["Über-Kategorie"] == ueberkat) & (df["Unter-Kategorie"] == unterkat)][i]
                for i in df["Hersteller"].loc[
                (df["Über-Kategorie"] == ueberkat) & (df["Unter-Kategorie"] == unterkat)].index
            ])))
        values = sorted(list(set(
            [
                df["Hersteller"].loc[(df["Über-Kategorie"] == ueberkat) & (df["Unter-Kategorie"] == unterkat)][i] +
                "," +
                df["Beschreibung"].loc[(df["Über-Kategorie"] == ueberkat) & (df["Unter-Kategorie"] == unterkat)][i] +
                "," +
                str(df["Leistung"].loc[(df["Über-Kategorie"] == ueberkat) & (df["Unter-Kategorie"] == unterkat)][i]) +
                "," +
                df["Kunststoffe"].loc[(df["Über-Kategorie"] == ueberkat) & (df["Unter-Kategorie"] == unterkat)][i]
                for i in df["Hersteller"].loc[
                (df["Über-Kategorie"] == ueberkat) & (df["Unter-Kategorie"] == unterkat)].index
            ])))

        output_1 = dcc.Input(id="Leistungswert", type="number", min=0, max=100000, persistence=True,
                             persistence_type='local', placeholder="Leistung in kW"), \
                   dcc.Input(id="Durchsatzwert", type="number", min=0, max=100000, persistence=True,
                             persistence_type='local', placeholder="Durchsatz in kg/h"), \
                   dcc.Dropdown(id="Dropdown-Maschinen", persistence=True, persistence_type='local',
                                placeholder="Daten für Maschine übernehmen",
                                options=[{'label': labels[i], 'value': values[i]} for i in range(len(labels))],
                                value="NA")
        return output_1, indizes
    else:
        output_1 = dcc.Input(id="Leistungswert", type="number", min=0, max=100000, persistence=True,
                             persistence_type='local', placeholder="Leistung in kW"), \
                   dcc.Input(id="Durchsatzwert", type="number", min=0, max=100000, persistence=True,
                             persistence_type='local', placeholder="Durchsatz in kg/h")
        return output_1, dash.no_update


@dash_app.callback(
    Output('tab-öffnen', 'label'), Output('tab-zerkleinern', 'label'),
    Output('tab-trennen', 'label'), Output('tab-waschen', 'label'), Output('tab-trocknen', 'label'),
    Output('tab-verdichten', 'label'), Output('tab-kombinierte', 'label'),

    Output("Gesamtemissionen", 'children'),
    Output('Geräteemissionen', 'children'),
    Output("Leistungswert", 'value'),
    Output("Durchsatzwert", 'value'),
    Output('Dropdown-Maschinen', 'value'),
    Output("Zwischenspeicher", 'data'),
    Output("Zwischenspeicher_Auswahl", 'data'),

    Input("Löschen", "n_clicks"),
    Input("Übernehmen", "n_clicks"),
    Input('Dropdown-Maschinen', 'value'),
    Input('Leistungswert', 'value'),
    Input('Durchsatzwert', 'value'),
    Input('Speicher_Indizes', 'data'),
    Input("Speicher_Emissionsmatrix", 'data'),
    Input("Speicher_Auswahl", 'data'),
    prevent_initial_call=True)  # Input('Ökostrom', 'value'),
def cb_trage_leistung_und_durchsatz_ein(delete, save, auswahl, leistung, durchsatz, ind, emissionsmatrix, speicher):
    for i in range(len(tab_labels)):
        if sum(emissionsmatrix[i]) > 0:
            tab_labels[i] = kategorien[i] + " %.4f kg CO2-e / kg" % sum(emissionsmatrix[i])
        else:
            tab_labels[i] = kategorien[i]
    # if oeko and oeko[0]=='Ökostrom': # Passe zunächst den Emissionsfaktor an, je nachdem, ob Ökostrom ausgewählt wurde
    #    print("Geändert")
    #    oekostromfaktor=0.2 # Faktor noch zu recherchieren
    # else:
    #    oekostromfaktor=1

    # print(oekostromfaktor)
    # for i in range(10):
    #    for j in range(10):
    #        emissionsmatrix[i][j] = emissionsmatrix[i][j] * oekostromfaktor
    # gesamtemissionen=sum([sum(c) for c in emissionsmatrix])
    indizes = ind

    changed_ids = [p['prop_id'].split('.')[0] for p in dash.callback_context.triggered]
    clear = 'Löschen' in changed_ids
    store = 'Übernehmen' in changed_ids

    data_storage = pd.read_json(speicher)
    print(data_storage.head())
    # Prüfe zunächst, ob hier schon Angaben gemacht wurden und trage diese dann automatisch wieder ein
    n = data_storage.query("i == %d & j== %d" % (indizes[0], indizes[1])).index[0]
    data = [data_storage["Auswahl"][n], data_storage["Leistung"][n], data_storage["Durchsatz"][n]]

    if changed_ids == ['Leistungswert', 'Durchsatzwert', 'Dropdown-Maschinen', 'Speicher_Indizes'] \
            or changed_ids == ['Übernehmen', 'Löschen', 'Leistungswert', 'Durchsatzwert',
                               'Dropdown-Maschinen', 'Speicher_Indizes']:
        if data != [np.nan, np.nan, np.nan]:
            auswahl = data[0]
            leistung = data[1]
            durchsatz = data[2]
            if durchsatz:
                emissionen = oekostromfaktor * (leistung * 0.366) / durchsatz
                return tab_labels[0], tab_labels[1], tab_labels[2], tab_labels[3], tab_labels[4], tab_labels[5], \
                       tab_labels[6], \
                       dash.no_update, "Emissionen pro kg: %.4f" % float(
                    emissionen) + " kg CO2-e", leistung, durchsatz, auswahl, emissionsmatrix, data_storage.to_json()
            else:
                return tab_labels[0], tab_labels[1], tab_labels[2], tab_labels[3], tab_labels[4], tab_labels[5], \
                       tab_labels[6], \
                       dash.no_update, "Emissionen: ", leistung, None, auswahl, emissionsmatrix, data_storage.to_json()

        else:
            return tab_labels[0], tab_labels[1], tab_labels[2], tab_labels[3], tab_labels[4], tab_labels[5], tab_labels[
                6], \
                   dash.no_update, "Emissionen: ", None, None, "NA", emissionsmatrix, data_storage.to_json()
            # Sorgt dafür, dass das Feld sonst immer leer ist

    if not clear:

        if store:  # Wenn die Auswahl gespeichert werden soll → Kein updaten mehr nötig
            if durchsatz:  # Division mit Null vermeiden
                emissionen = oekostromfaktor * (leistung * 0.366) / durchsatz
                emissionsmatrix[indizes[0]][indizes[1]] = emissionen

                # Daten aktualisieren und speichern
                gesamtemissionen = sum([sum(c) for c in emissionsmatrix])

                data_storage["Auswahl"].loc[
                    (data_storage["i"] == int(indizes[0])) & (data_storage["j"] == int(indizes[1]))] = auswahl
                data_storage["Leistung"].loc[
                    (data_storage["i"] == int(indizes[0])) & (data_storage["j"] == int(indizes[1]))] = leistung
                data_storage["Durchsatz"].loc[
                    (data_storage["i"] == int(indizes[0])) & (data_storage["j"] == int(indizes[1]))] = durchsatz

                return tab_labels[0], tab_labels[1], tab_labels[2], tab_labels[3], tab_labels[4], tab_labels[5], \
                       tab_labels[6], \
                       "Gesamtemissionen pro kg: %.4f" % float(
                           gesamtemissionen) + " kg CO2-e", "Emissionen pro kg: %.4f" % float(
                    emissionen) + " kg CO2-e", leistung, durchsatz, dash.no_update, emissionsmatrix, data_storage.to_json()
            else:
                return tab_labels[0], tab_labels[1], tab_labels[2], tab_labels[3], tab_labels[4], tab_labels[5], \
                       tab_labels[6], \
                       dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, emissionsmatrix, data_storage.to_json()

        else:  # Aktualisiere Werte hier
            if auswahl and auswahl != "NA" and 'Dropdown-Maschinen' in changed_ids:  # not durchsatz and not leistung:
                hersteller = auswahl.split(",")[0]
                beschreibung = auswahl.split(",")[1]
                leistung = float(auswahl.split(",")[2])
                emissionen = list(df["Emissionen"].loc[
                                      (df["Hersteller"] == hersteller) & (df["Beschreibung"] == beschreibung) & (
                                              df["Leistung"] == leistung)])[0]
                if emissionen != "#DIV/0!":
                    emissionen = oekostromfaktor * float(emissionen)

                if not np.isnan(list(df["Durchsatzleistung"].loc[
                                         (df["Hersteller"] == hersteller) & (df["Beschreibung"] == beschreibung) & (
                                                 df["Leistung"] == leistung)])[0]):
                    durchsatz = float(list(df["Durchsatzleistung"].loc[(df["Hersteller"] == hersteller) & (
                            df["Beschreibung"] == beschreibung) & (df["Leistung"] == leistung)])[0])

                if np.isnan(list(df["Durchsatzleistung"].loc[
                                     (df["Hersteller"] == hersteller) & (df["Beschreibung"] == beschreibung) & (
                                             df["Leistung"] == leistung)])[0]):
                    durchsatz = None

                if emissionen == "#DIV/0!" and leistung and durchsatz:
                    emissionen = oekostromfaktor * (leistung * 0.366) / durchsatz

                if durchsatz:  # Wenn in den Daten eine Angabe zum Durchsatz ist
                    return tab_labels[0], tab_labels[1], tab_labels[2], tab_labels[3], tab_labels[4], tab_labels[5], \
                           tab_labels[6], \
                           dash.no_update, "Emissionen pro kg: %.4f" % float(
                        emissionen) + " kg CO2-e", leistung, durchsatz, dash.no_update, emissionsmatrix, data_storage.to_json()

                if not durchsatz:  # Wenn das nicht der Fall ist, setze den Durchsatz auf none
                    return tab_labels[0], tab_labels[1], tab_labels[2], tab_labels[3], tab_labels[4], tab_labels[5], \
                           tab_labels[6], \
                           dash.no_update, "Emissionen: ", leistung, None, dash.no_update, emissionsmatrix, data_storage.to_json()

            elif len(changed_ids) < 2 and 'Leistungswert' in changed_ids or 'Durchsatzwert' in changed_ids:
                if durchsatz and leistung:
                    emissionen = oekostromfaktor * (leistung * 0.366) / durchsatz
                    return tab_labels[0], tab_labels[1], tab_labels[2], tab_labels[3], tab_labels[4], tab_labels[5], \
                           tab_labels[6], \
                           dash.no_update, "Emissionen pro kg: %.4f" % float(
                        emissionen) + " kg CO2-e", leistung, durchsatz, dash.no_update, emissionsmatrix, data_storage.to_json()

                else:
                    return tab_labels[0], tab_labels[1], tab_labels[2], tab_labels[3], tab_labels[4], tab_labels[5], \
                           tab_labels[6], \
                           dash.no_update, dash.no_update, dash.no_update, \
                           dash.no_update, dash.no_update, emissionsmatrix, data_storage.to_json()

    if clear:
        emissionsmatrix[int(indizes[0])][int(indizes[1])] = 0
        gesamtemissionen = sum([sum(c) for c in emissionsmatrix])
        data_storage["Auswahl"].loc[
            (data_storage["i"] == int(indizes[0])) & (data_storage["j"] == int(indizes[1]))] = np.nan
        data_storage["Leistung"].loc[
            (data_storage["i"] == int(indizes[0])) & (data_storage["j"] == int(indizes[1]))] = np.nan
        data_storage["Durchsatz"].loc[
            (data_storage["i"] == int(indizes[0])) & (data_storage["j"] == int(indizes[1]))] = np.nan

        return tab_labels[0], tab_labels[1], tab_labels[2], tab_labels[3], tab_labels[4], tab_labels[5], tab_labels[6], \
               "Gesamtemissionen pro kg: %.4f" % float(gesamtemissionen) + " kg CO2-e", \
               "Emissionen: ", None, None, "NA", emissionsmatrix, data_storage.to_json()


@dash_app.callback(Output("Speicher_Emissionsmatrix", 'data'),
              Output("Speicher_Auswahl", 'data'),
              Input("Zwischenspeicher", 'data'),
              Input("Zwischenspeicher_Auswahl", 'data'),
              prevent_initial_callback=True)
def uebertrage_daten(data1, data2):
    return data1, data2


# Ergebnisse plotten, wenn der entsprechende Button gedrückt wird


@dash_app.callback(Output(component_id="Ergebnisgrafik", component_property='figure'),
              Input("Button-Ergebnisse", "n_clicks"),
              Input("Speicher_Emissionsmatrix", 'data'),
              prevent_initial_callback=True)
def plot(btn, emissionsmatrix):
    changed_ids = [p['prop_id'].split('.')[0] for p in dash.callback_context.triggered]
    if "Button-Ergebnisse" in changed_ids:
        kat = ['Öffnen, Auflösen', 'Zerkleinern', 'Trennen', 'Waschen', 'Trocknen', 'Agglomerieren, Verdichten',
               'Kombinierte Anlagen']
        ukat = [list(set(df["Unter-Kategorie"].loc[df["Über-Kategorie"] == k])) for k in kat]
        a = emissionsmatrix
        T = []
        Y = []
        K = []
        UK = []
        for i in range(len(kat)):
            ind = np.asarray(a[i]).nonzero()[0]
            for j in ind:
                Y.append(float(a[i][j]))
                UK.append(ukat[i][j])
                K.append(kat[i])
                T.append("Gesamtemissionen")

        plotdaten = pd.DataFrame({"Überkategorie": K, "Unterkategorie": UK, "Emissionen": Y, "Gesamtemissionen": T})

        fig = px.sunburst(plotdaten, path=["Gesamtemissionen", "Überkategorie", "Unterkategorie"], values="Emissionen",
                          title="Zusammensetzung der Emissionen des Recyclingprozesses", width=750, height=750,
                          color_discrete_sequence=wi_colors)
        fig.update_traces(hovertemplate="%{label}<br>Emissionen: %{value:.4f} kg CO2-e / kg<br>")

        return fig
    else:
        raise PreventUpdate  # dash.no_update


# Ergebnisse als CSV exportieren

@dash_app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn_csv", "n_clicks"),
    Input("Speicher_Emissionsmatrix", 'data'),
    prevent_initial_call=True,
)
def func(n_clicks, emissionsmatrix):
    changed_ids = [p['prop_id'].split('.')[0] for p in dash.callback_context.triggered]
    if "btn_csv" in changed_ids:
        kat = ['Öffnen, Auflösen', 'Zerkleinern', 'Trennen', 'Waschen', 'Trocknen', 'Agglomerieren, Verdichten',
               'Kombinierte Anlagen']
        ukat = [list(set(df["Unter-Kategorie"].loc[df["Über-Kategorie"] == k])) for k in kat]
        a = emissionsmatrix
        Y = []
        K = []
        UK = []
        for i in range(len(kat)):
            ind = np.asarray(a[i]).nonzero()[0]
            for j in ind:
                Y.append(float(a[i][j]))
                UK.append(ukat[i][j])
                K.append(kat[i])

        exportdaten = pd.DataFrame({"Überkategorie": K, "Unterkategorie": UK, "Emissionen (kg CO2-e / kg)": Y})

        return dcc.send_data_frame(exportdaten.to_excel, "Emissionen_Recyclingprozess.xlsx",
                                   sheet_name="Emissionen der Prozessschritte")
    else:
        raise PreventUpdate  # dash.no_update


if __name__ == "__main__":
    dash_app.run_server(debug=False)
