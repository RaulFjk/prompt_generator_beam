import requests
import json

def test_extraction():

    url = "http://localhost:8000/test_extraction"

    # 1) Provide the final_prompt from your prior test
    final_prompt = """Final prompt comes here"""

    # 2) Provide the a parsed doc as text.
    file_content_snippet = r'''{
  "dataset": "<figure>\n\nSiadler\nDeutschlands größtes Zweirad-Center\n\n</figure>\n\n\nwww.zweirad-stadler.de\n\n\n<table>\n<tr>\n<th>· Berlin Charlottenburg</th>\n<th>· Mönchengladbach</th>\n<th>· Nürnberg</th>\n</tr>\n<tr>\n<td>· Berlin Prenzlauer Berg</td>\n<td>· Leipzig/Halle</td>\n<td>· Fürth</td>\n</tr>\n<tr>\n<td>· Bremen</td>\n<td>· Leipzig Alte Messe</td>\n<td>· Regensburg</td>\n</tr>\n<tr>\n<td>· Hannover</td>\n<td>· Chemnitz</td>\n<td>· Straubing</td>\n</tr>\n<tr>\n<td>· Essen</td>\n<td>· Mülheim-Kärlich</td>\n<td>· Filderstadt</td>\n</tr>\n<tr>\n<td>· Düsseldorf Eller</td>\n<td>· Frankfurt a. M.</td>\n<td>· Hammerau</td>\n</tr>\n<tr>\n<td>· Düsseldorf Am Wehrhahn</td>\n<td>· Mannheim</td>\n<td>· München</td>\n</tr>\n</table>\n\n\nZweirad-Center Stadler, Straße des 18. Oktober 46, 04103 Leipzig\n\nHerr\nJens Walter\nLausnerweg 45\n04207 Leipzig\n\nKDNR\n\n\n<table>\n<tr>\n<th>Rechnungsdatum</th>\n<th>Verkaufsnr .:</th>\n<th>Lieferschein Nr .:</th>\n<th>Liefer-/Abholdatum:</th>\n<th>Kundennr .:</th>\n</tr>\n<tr>\n<td>22.02.2024</td>\n<td>44828</td>\n<td>40923</td>\n<td>Do, 22.02.2024</td>\n<td>44124</td>\n</tr>\n</table>\n\n\n<table>\n<tr>\n<td>Telefon:</td>\n<td>0341/</td>\n</tr>\n<tr>\n<td>Mobil:</td>\n<td>+49 171 7803957</td>\n</tr>\n<tr>\n<td>Telefax:</td>\n<td>0341/</td>\n</tr>\n<tr>\n<td>E-Mail:</td>\n<td>js.walter@gmx.net</td>\n</tr>\n<tr>\n<td></td>\n<td>Stellplatz: 349</td>\n</tr>\n</table>\n\n\n# Rechnung Nummer 43703\n\nBetreff:\nPegasus Trekking\n\n\n<table>\n<tr>\n<th>Menge</th>\n<th>Bezeichnung</th>\n<th>Artikelnr.</th>\n<th>Preis EUR</th>\n<th>Wert EUR</th>\n</tr>\n<tr>\n<td colspan=\"2\">Material:</td>\n<td></td>\n<td></td>\n<td></td>\n</tr>\n<tr>\n<td rowspan=\"2\">1</td>\n<td># BREMSSCHEIBE 6-Loch 160MM, SMRT66 Metal/Resin</td>\n<td>307524</td>\n<td>19,99</td>\n<td>19,99</td>\n</tr>\n<tr>\n<td>Shimano BREMSSCHEIBE 160mm 6-loch (Artlief. ESMRT66S)</td>\n<td></td>\n<td></td>\n<td></td>\n</tr>\n<tr>\n<td>1</td>\n<td># BREMSSCHEIBE 6-Loch 180MM, SMRT66 Metal/Resin</td>\n<td>307523</td>\n<td>21,99</td>\n<td>21,99</td>\n</tr>\n<tr>\n<td></td>\n<td>Shimano BREMSSCHEIBE 180mm 6-loch (Artlief. ESMRT66M)</td>\n<td></td>\n<td></td>\n<td></td>\n</tr>\n<tr>\n<td rowspan=\"2\">1</td>\n<td># ADAPT. SATZ F DISC-BR MIT SCHRAUBEN</td>\n<td>305643</td>\n<td>8,99</td>\n<td>8,99</td>\n</tr>\n<tr>\n<td>Adapter Satz für Discbrake mit Schrauben, PM 180mm (Artlief. ESMMAF180PP2A)</td>\n<td></td>\n<td></td>\n<td></td>\n</tr>\n<tr>\n<td rowspan=\"2\">1</td>\n<td>Scheibenbremse MT501 2-Kolben,HR, I-Spec II, Resin</td>\n<td>311381</td>\n<td rowspan=\"2\">69,99</td>\n<td rowspan=\"2\">69,99</td>\n</tr>\n<tr>\n<td>Scheibenbremse MT501 HR, I-Spec II, Resin B05S (Artlief. EMT5012JRRXRA170)</td>\n<td></td>\n</tr>\n<tr>\n<td rowspan=\"2\">1</td>\n<td>Scheibenbremse MT501 2-Kolben, VR, I-Spec II, Resin</td>\n<td>311823</td>\n<td rowspan=\"2\">64,99</td>\n<td rowspan=\"2\">64,99</td>\n</tr>\n<tr>\n<td>Scheibenbremse MT501 VR, I-Spec II, Resin B05S (Artlief. EMT5012JLFPRA100)</td>\n<td></td>\n</tr>\n<tr>\n<td rowspan=\"2\">1</td>\n<td># Kette CN-HG71 6/7/8-fach, 138 Glieder</td>\n<td>248956</td>\n<td rowspan=\"2\">21,99</td>\n<td rowspan=\"2\">21,99</td>\n</tr>\n<tr>\n<td>Shimano Kette CN-HG71 6/7/8-F 138 Glieder (Artlief. ECNHG71C1381)</td>\n<td></td>\n</tr>\n<tr>\n<td>1</td>\n<td># KASSETTE HG51 8F.11-32Z Shimano Kassette HG51 8-fach, 11-32 Zähne (Artlief. ECSHG518132)</td>\n<td>457471</td>\n<td>21,99</td>\n<td>21,99</td>\n</tr>\n<tr>\n<td></td>\n<td></td>\n<td></td>\n<td>Summe:</td>\n<td>229,93</td>\n</tr>\n</table>\n\n\nZweirad-Center Stadler Leipzig Alte Messe GmbH\nStraße des 18. Oktober 46\n04103 Leipzig\nEingetragen im Registergericht:\nLeipzig HRB 35591\nGeschäftsführer: Bärbel Stadler,\nCaroline Elleke\n\nTelefon: +49 (0) 341 / 212068 - 0\nVerkauf: +49 (0) 341 / 212068 - 128\nWerkstatt: +49 (0) 341 / 212068 - 129\nTelefax: +49 (0) 341 / 212068 - 137\nlam@zweirad-stadler.de\nwww.zweirad-stadler.de\n\nPostbank\nIBAN: DE72760100850162069856\nBIC: PBNKDEFFXXX\nUSt-ID: DE321559864\nSteuernr .: 231/123/04576\n\n<!-- PageNumber=\"1 von 2\" -->\n\n08 neutral 05.21\n\n<!-- PageBreak -->\n\n\n<figure>\n\nStadler\nDeutschlands größtes Zweirad-Center\n\n</figure>\n\n\nwww.zweirad-stadler.de\n\n\n<table>\n<tr>\n<th>· Berlin Charlottenburg</th>\n<th>· Mönchengladbach</th>\n<th>· Nürnberg</th>\n</tr>\n<tr>\n<td>· Berlin Prenzlauer Berg</td>\n<td>· Leipzig/Halle</td>\n<td>· Fürth</td>\n</tr>\n<tr>\n<td>· Bremen</td>\n<td>· Leipzig Alte Messe</td>\n<td>· Regensburg</td>\n</tr>\n<tr>\n<td>· Hannover</td>\n<td>· Chemnitz</td>\n<td>· Straubing</td>\n</tr>\n<tr>\n<td>· Essen</td>\n<td>· Mülheim-Kärlich</td>\n<td>· Filderstadt</td>\n</tr>\n<tr>\n<td>· Düsseldorf Eller</td>\n<td>· Frankfurt a. M.</td>\n<td>· Hammerau</td>\n</tr>\n<tr>\n<td>· Düsseldorf Am Wehrhahn</td>\n<td>· Mannheim</td>\n<td>· München</td>\n</tr>\n</table>\n\n\nZweirad-Center Stadler, Straße des 18. Oktober 46, 04103 Leipzig\n\nHerr\nJens Walter\nLausnerweg 45\n04207 Leipzig\n\nKDNR\n\n\n<table>\n<tr>\n<th>Rechnungsdatum</th>\n<th>Verkaufsnr .:</th>\n<th>Lieferschein Nr .:</th>\n<th>Liefer-/Abholdatum:</th>\n<th>Kundennr .:</th>\n</tr>\n<tr>\n<td>22.02.2024</td>\n<td>44828</td>\n<td>40923</td>\n<td>Do, 22.02.2024</td>\n<td>44124</td>\n</tr>\n</table>\n\n\n<table>\n<tr>\n<td>Telefon:</td>\n<td>0341/</td>\n</tr>\n<tr>\n<td>Mobil:</td>\n<td>+49 171 7803957</td>\n</tr>\n<tr>\n<td>Telefax:</td>\n<td>0341/</td>\n</tr>\n<tr>\n<td>E-Mail:</td>\n<td>js.walter@gmx.net</td>\n</tr>\n</table>\n\n\n## Rechnung Nummer 43703\n\n\n<table>\n<tr>\n<th>Menge</th>\n<th>Bezeichnung</th>\n<th>Artikelnr.</th>\n<th>Preis EUR</th>\n<th>Wert EUR</th>\n</tr>\n<tr>\n<td colspan=\"2\">Arbeitsbeschreibung:</td>\n<td></td>\n<td colspan=\"2\"></td>\n</tr>\n<tr>\n<td>15</td>\n<td>Bremsscheibe erneuern vorn zzgl. Material 203mm</td>\n<td>217.00</td>\n<td>1,90</td>\n<td>28,50</td>\n</tr>\n<tr>\n<td>15</td>\n<td>Bremsscheibe erneuern hinten zzgl. Material</td>\n<td>218.00</td>\n<td>1,90</td>\n<td>28,50</td>\n</tr>\n<tr>\n<td>40</td>\n<td>Hydraulische Bremsanlage montieren vorn&amp;hinten zzgl.Mat</td>\n<td>230.00</td>\n<td>1,90</td>\n<td>76,00</td>\n</tr>\n<tr>\n<td>20</td>\n<td>Kette &amp; Kassette wechseln zzgl. Material</td>\n<td>10.00</td>\n<td>1,90</td>\n<td>38,00</td>\n</tr>\n<tr>\n<td></td>\n<td>Klein- und Reinigungsmaterial</td>\n<td>903.00</td>\n<td></td>\n<td>F. 2,49</td>\n</tr>\n<tr>\n<td></td>\n<td>Altteile dürfen entsorgt werden</td>\n<td>904.00</td>\n<td></td>\n<td>F. 0.00</td>\n</tr>\n<tr>\n<td></td>\n<td colspan=\"4\">Summe: 173,49</td>\n</tr>\n</table>\n\n\n<table>\n<tr>\n<td>Summe</td>\n<td>403,42</td>\n</tr>\n<tr>\n<td>Noch zu zahlen</td>\n<td>403,42</td>\n</tr>\n</table>\n\n\nEnthaltene Mehrwertsteuer:\n19,00 % MwSt (= EUR 64,41) auf EUR 339,01\n\nAuftragsannahme erfolgte durch Kehrer-Liebmann Michael.\nIhre Reparatur wurde ausgeführt von Chmieleski Sebastian.\n\nZweirad-Center Stadler Leipzig Alte Messe GmbH\nStraße des 18. Oktober 46\n04103 Leipzig\nEingetragen im Registergericht:\nLeipzig HRB 35591\nGeschäftsführer: Bärbel Stadler,\n\n<!-- PageFooter=\"Telefon: +49 (0) 341 / 212068 - 0\" -->\n\nVerkauf: +49 (0) 341 / 212068 - 128\nWerkstatt: +49 (0) 341 / 212068 - 129\nTelefax: +49 (0) 341 / 212068 - 137\nlam@zweirad-stadler.de\nwww.zweirad-stadler.de\n\nPostbank\nIBAN: DE72760100850162069856\n\nBIC: PBNKDEFFXXX\n\nUSt-ID: DE321559864\n\nSteuernr .: 231/123/04576\n\nCaroline Elleke\n\n<!-- PageNumber=\"2 von 2\" -->\n\n08 neutral 05.21",
  "output_format": "# *Respond exactly in the following perfectly formatted JSON structure with no missing fields*:\n{\n  \"parsed_data\": \"string // The parsed data extracted from the dataset, organized and categorized based on predefined criteria.\"\n}"
}'''

    # Parse the JSON snippet
    try:
        parsed_obj = json.loads(file_content_snippet)
    except json.JSONDecodeError as e:
        print("Error parsing the snippet JSON:", e)
        return

    if "dataset" not in parsed_obj:
        print("Error: 'dataset' key not found in the provided JSON snippet.")
        return

    dataset_content = parsed_obj["dataset"]

    # Prepare the payload for /test_extraction
    payload = {
        "final_prompt": final_prompt,
        "file_content": dataset_content  
    }

    print(f"Sending test request to {url} ...")
    response = requests.post(url, json=payload)
    print("Status Code:", response.status_code)

    if response.status_code == 200:
        result = response.json()
        print("Response JSON:\n", json.dumps(result, indent=2))
        print("\nExtraction Result:\n", result["extraction_result"])
    else:
        print("Error response:", response.text)

if __name__ == "__main__":
    test_extraction()
