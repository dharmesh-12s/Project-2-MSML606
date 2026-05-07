import pandas as pd
import networkx as nx
import json

df = pd.read_csv("supply_chain_clean.csv")

# Load translations
with open("city_translations.json", "r", encoding="utf-8") as f:
    city_translation = json.load(f)

country_translation = {
    'Afganistán': 'Afghanistan', 'Albania': 'Albania', 'Alemania': 'Germany',
    'Angola': 'Angola', 'Arabia Saudí': 'Saudi Arabia', 'Argelia': 'Algeria',
    'Argentina': 'Argentina', 'Australia': 'Australia', 'Austria': 'Austria',
    'Azerbaiyán': 'Azerbaijan', 'Bangladés': 'Bangladesh', 'Barbados': 'Barbados',
    'Belice': 'Belize', 'Benín': 'Benin', 'Bielorrusia': 'Belarus',
    'Bolivia': 'Bolivia', 'Bosnia y Herzegovina': 'Bosnia and Herzegovina',
    'Botsuana': 'Botswana', 'Brasil': 'Brazil', 'Bulgaria': 'Bulgaria',
    'Burkina Faso': 'Burkina Faso', 'Bélgica': 'Belgium', 'Camboya': 'Cambodia',
    'Camerún': 'Cameroon', 'Canada': 'Canada', 'Chad': 'Chad', 'Chile': 'Chile',
    'China': 'China', 'Chipre': 'Cyprus', 'Colombia': 'Colombia',
    'Corea del Sur': 'South Korea', 'Costa Rica': 'Costa Rica',
    'Costa de Marfil': 'Ivory Coast', 'Croacia': 'Croatia', 'Cuba': 'Cuba',
    'Dinamarca': 'Denmark', 'Ecuador': 'Ecuador', 'Egipto': 'Egypt',
    'El Salvador': 'El Salvador', 'Emiratos Árabes Unidos': 'UAE',
    'Eslovaquia': 'Slovakia', 'Eslovenia': 'Slovenia', 'España': 'Spain',
    'Estados Unidos': 'United States', 'Estonia': 'Estonia', 'Etiopía': 'Ethiopia',
    'Filipinas': 'Philippines', 'Finlandia': 'Finland', 'Francia': 'France',
    'Gabón': 'Gabon', 'Georgia': 'Georgia', 'Ghana': 'Ghana', 'Grecia': 'Greece',
    'Guadalupe': 'Guadeloupe', 'Guatemala': 'Guatemala',
    'Guayana Francesa': 'French Guiana', 'Guinea': 'Guinea',
    'Guinea-Bissau': 'Guinea-Bissau', 'Guyana': 'Guyana', 'Haití': 'Haiti',
    'Honduras': 'Honduras', 'Hong Kong': 'Hong Kong', 'Hungría': 'Hungary',
    'India': 'India', 'Indonesia': 'Indonesia', 'Irak': 'Iraq',
    'Irlanda': 'Ireland', 'Irán': 'Iran', 'Israel': 'Israel', 'Italia': 'Italy',
    'Jamaica': 'Jamaica', 'Japón': 'Japan', 'Jordania': 'Jordan',
    'Kazajistán': 'Kazakhstan', 'Kenia': 'Kenya', 'Kirguistán': 'Kyrgyzstan',
    'Laos': 'Laos', 'Lesoto': 'Lesotho', 'Liberia': 'Liberia', 'Libia': 'Libya',
    'Lituania': 'Lithuania', 'Luxemburgo': 'Luxembourg', 'Líbano': 'Lebanon',
    'Macedonia': 'Macedonia', 'Madagascar': 'Madagascar', 'Malasia': 'Malaysia',
    'Mali': 'Mali', 'Marruecos': 'Morocco', 'Martinica': 'Martinique',
    'Mauritania': 'Mauritania', 'Moldavia': 'Moldova', 'Mongolia': 'Mongolia',
    'Montenegro': 'Montenegro', 'Mozambique': 'Mozambique',
    'Myanmar (Birmania)': 'Myanmar', 'México': 'Mexico', 'Namibia': 'Namibia',
    'Nepal': 'Nepal', 'Nicaragua': 'Nicaragua', 'Nigeria': 'Nigeria',
    'Noruega': 'Norway', 'Nueva Zelanda': 'New Zealand', 'Níger': 'Niger',
    'Omán': 'Oman', 'Pakistán': 'Pakistan', 'Panamá': 'Panama',
    'Papúa Nueva Guinea': 'Papua New Guinea', 'Paraguay': 'Paraguay',
    'Países Bajos': 'Netherlands', 'Perú': 'Peru', 'Polonia': 'Poland',
    'Portugal': 'Portugal', 'Qatar': 'Qatar', 'Reino Unido': 'United Kingdom',
    'República Centroafricana': 'Central African Republic',
    'República Checa': 'Czech Republic',
    'República Democrática del Congo': 'DR Congo',
    'República Dominicana': 'Dominican Republic',
    'República de Gambia': 'Gambia', 'República del Congo': 'Republic of Congo',
    'Ruanda': 'Rwanda', 'Rumania': 'Romania', 'Rusia': 'Russia',
    'Senegal': 'Senegal', 'Sierra Leona': 'Sierra Leone', 'Singapur': 'Singapore',
    'Siria': 'Syria', 'Somalia': 'Somalia', 'Sri Lanka': 'Sri Lanka',
    'Suazilandia': 'Eswatini', 'SudAfrica': 'South Africa', 'Sudán': 'Sudan',
    'Suecia': 'Sweden', 'Suiza': 'Switzerland', 'Surinam': 'Suriname',
    'Tailandia': 'Thailand', 'Taiwán': 'Taiwan', 'Tanzania': 'Tanzania',
    'Tayikistán': 'Tajikistan', 'Togo': 'Togo', 'Trinidad y Tobago': 'Trinidad and Tobago',
    'Turkmenistán': 'Turkmenistan', 'Turquía': 'Turkey', 'Túnez': 'Tunisia',
    'Ucrania': 'Ukraine', 'Uganda': 'Uganda', 'Uruguay': 'Uruguay',
    'Uzbekistán': 'Uzbekistan', 'Venezuela': 'Venezuela', 'Vietnam': 'Vietnam',
    'Yemen': 'Yemen', 'Yibuti': 'Djibouti', 'Zambia': 'Zambia', 'Zimbabue': 'Zimbabwe'
}

df['Market'] = df['Market'].str.strip()
df['Order Region'] = df['Order Region'].str.strip() + " (Region)"
df['Order Country'] = df['Order Country'].str.strip().map(country_translation) + " (Country)"
df['Order City'] = df['Order City'].str.strip().map(city_translation) + " (City)"

def build_graph(df):
    G = nx.DiGraph()
    for level_a, level_b in [
        ('Market', 'Order Region'),
        ('Order Region', 'Order Country'),
        ('Order Country', 'Order City')
    ]:
        agg = df.groupby([level_a, level_b]).agg(
            avg_days=('Days for shipping (real)', 'mean'),
            avg_cost=('Order Item Total', 'mean'),
        ).reset_index()
        for _, row in agg.iterrows():
            G.add_edge(row[level_a], row[level_b],
                       avg_days=round(row['avg_days'], 2),
                       avg_cost=round(row['avg_cost'], 2))
    return G

G = build_graph(df)

print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())
print("Is DAG:", nx.is_directed_acyclic_graph(G))

nx.write_gml(G, "supply_chain_graph_v3.gml")
print("Saved: supply_chain_graph_v3.gml")