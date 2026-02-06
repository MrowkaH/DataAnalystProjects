from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register a font that supports Polish characters
pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', 'DejaVuSans-Bold.ttf'))

def create_study_plan_pdf(filename):
    doc = SimpleDocTemplate(filename, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    elements = []

    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitlePL',
        parent=styles['Title'],
        fontName='DejaVuSans-Bold',
        fontSize=18,
        spaceAfter=20,
        alignment=1 # Center
    )
    h1_style = ParagraphStyle(
        'Heading1PL',
        parent=styles['Heading2'],
        fontName='DejaVuSans-Bold',
        fontSize=14,
        spaceBefore=15,
        spaceAfter=10,
        textColor=colors.darkblue
    )
    normal_style = ParagraphStyle(
        'NormalPL',
        parent=styles['Normal'],
        fontName='DejaVuSans',
        fontSize=10,
        leading=14
    )
    bullet_style = ParagraphStyle(
        'BulletPL',
        parent=styles['Normal'],
        fontName='DejaVuSans',
        fontSize=10,
        leading=14,
        bulletIndent=10,
        leftIndent=20
    )

    # --- TITLE PAGE ---
    elements.append(Paragraph("PLAN NAUKI DO EGZAMINU INŻYNIERSKIEGO", title_style))
    elements.append(Paragraph("Informatyka (MiTI) - UKEN", title_style))
    elements.append(Spacer(1, 20))
    
    intro_text = """
    <b>Cel:</b> Zdać egzamin inżynierski (pisemny i ustny).<br/>
    <b>Start:</b> 16 Grudnia 2024.<br/>
    <b>Meta:</b> 1 Lutego 2025.<br/>
    <b>Strategia:</b> Zrozumienie kluczowych pojęć (pod ustny) + Testy (pod pisemny).
    """
    elements.append(Paragraph(intro_text, normal_style))
    elements.append(Spacer(1, 20))

    # --- DAILY ROUTINE ---
    elements.append(Paragraph("1. RUTYNA DNIA (Dni Robocze)", h1_style))
    routine_data = [
        ["Godziny", "Typ Bloku", "Opis Działania"],
        ["10:00 - 13:00", "BLOK GŁĘBOKI\n(Teoria)", "Najtrudniejsze tematy. Czytanie, oglądanie, notatki.\nCel: Umieć opowiedzieć na głos."],
        ["13:00 - 14:00", "PRZERWA", "Obiad, spacer, reset głowy."],
        ["14:00 - 17:00", "BLOK PRAKTYCZNY\n(Konkrety)", "Pisanie zapytań SQL, analiza kodu, schematy sieci,\nzagadnienia z grafiki/multimediów."],
        ["19:00 - 20:30", "TESTY (ABCD)", "Rozwiązywanie pytań z plików PDF (baza pytań).\nNauka pod egzamin pisemny."]
    ]
    
    t_routine = Table(routine_data, colWidths=[80, 110, 320])
    t_routine.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(t_routine)
    elements.append(Spacer(1, 20))

    # --- SCHEDULE ---
    elements.append(Paragraph("2. HARMONOGRAM (KALENDARZ)", h1_style))
    
    # Data for the schedule table
    schedule_data = [
        ["Data", "Dział / Temat", "Szczegóły (Co umieć?)"],
        # Week 1
        ["16-17.12\n(Pon-Wt)", "BAZY DANYCH\n(SQL)", "SELECT (kolejność), JOIN (Inner/Left/Right),\nFunkcje agregujące, GROUP BY, HAVING."],
        ["18-19.12\n(Śr-Czw)", "BAZY DANYCH\n(Teoria)", "Normalizacja (I, II, III postać), Klucze (PK, FK),\nACID, Transakcje, Indeksy."],
        ["20.12\n(Piątek)", "TESTY BAZY", "Wszystkie pytania ABCD z baz danych (PDF)."],
        # Week 2
        ["21-22.12\n(Sob-Ndz)", "WEB (Backend)", "HTTP (GET/POST), Kody (200, 404, 500),\nCookies vs Session, MVC, REST API."],
        ["23.12\n(Pon)", "WEB (Frontend)", "DOM, RWD (Media Queries), WCAG 2.1,\nZnaczniki HTML, CSS Box Model."],
        ["24-26.12", "ŚWIĘTA", "WOLNE - Odpocznij!"],
        # Week 3
        ["27.12\n(Piątek)", "SIECI (Model OSI)", "7 warstw OSI (nazwy i funkcje),\nTCP vs UDP (różnice)."],
        ["28.12\n(Sobota)", "SIECI (Adresacja)", "IPv4 vs IPv6, Maska podsieci, DNS, DHCP,\nRouter vs Switch."],
        ["29-30.12\n(Ndz-Pon)", "SYSTEMY (Linux)", "Prawa dostępu (chmod), Proces vs Wątek,\nStruktura katalogów, Podstawowe komendy."],
        ["31.12-01.01", "SYLWESTER", "WOLNE"],
        # Week 4 - Hardcore
        ["02-03.01\n(Czw-Pt)", "ALGORYTMY", "Złożoność O(n), Sortowanie (idee),\nStos, Kolejka, Drzewa."],
        ["04-06.01\n(Sob-Pon)", "PROGRAMOWANIE\n(OOP)", "4 Filary: Abstrakcja, Hermetyzacja,\nDziedziczenie, Polimorfizm. Klasa vs Obiekt."],
        ["07-08.01\n(Wt-Śr)", "INŻ. OPROGR.", "Wzorce (Singleton, Fabryka, MVC),\nMetodyki (Scrum, Waterfall), UML."],
        # Week 5 - Specjalizacja
        ["09-11.01\n(Czw-Sob)", "GRAFIKA (MiTI)", "Wektorowa vs Rastrowa, RGB vs CMYK,\nKompresja, Histogram, Filtry, Binaryzacja."],
        ["12-13.01\n(Ndz-Pon)", "SPRZĘT / HW", "RAM vs SSD, Bramki logiczne,\nDioda, Tranzystor, Mikrokontrolery."],
        ["14-15.01\n(Wt-Śr)", "TESTY MiTI/ASI", "Rozwiązywanie testów specjalizacyjnych (PDF)."],
        # Week 6 - Math & Final
        ["16-18.01\n(Czw-Sob)", "MATEMATYKA", "Logika (zbiory), Funkcje (iniekcja),\nGranice, Pochodne (definicje)."],
        ["19-22.01\n(Ndz-Śr)", "FIZYKA / TEORIA", "System dwójkowy/szesnastkowy,\nOptyka (światłowody), Macierze."],
        # Simulation
        ["23.01-01.02", "SYMULACJA", "Codziennie: 3 pytania ustne (na głos)\n+ 1 pełny test ABCD na czas."]
    ]

    t_schedule = Table(schedule_data, colWidths=[70, 120, 320])
    t_schedule.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.white])
    ]))
    elements.append(t_schedule)
    elements.append(PageBreak())

    # --- CHEAT SHEET ---
    elements.append(Paragraph("3. ŚCIĄGA TEMATYCZNA (Baza Wiedzy)", h1_style))
    elements.append(Paragraph("Najważniejsze pojęcia, które musisz znać na pamięć.", normal_style))
    elements.append(Spacer(1, 10))

    cheat_sheet = [
        ("BAZY DANYCH", [
            "Kolejność SQL: SELECT -> FROM -> WHERE -> GROUP BY -> HAVING -> ORDER BY",
            "INNER JOIN: Tylko rekordy pasujące w obu tabelach.",
            "LEFT JOIN: Wszystkie z lewej + pasujące z prawej (reszta NULL).",
            "ACID: Atomowość (wszystko albo nic), Spójność, Izolacja, Trwałość.",
            "Normalizacja: I (atomowe wartości), II (klucz główny), III (brak zależności przechodnich)."
        ]),
        ("SIECI KOMPUTEROWE", [
            "Model OSI (7 warstw): Fizyczna, Łącza, Sieci (Router/IP), Transportowa (TCP), Sesji, Prezentacji, Aplikacji.",
            "TCP vs UDP: TCP gwarantuje dostarczenie (wolniejszy), UDP nie gwarantuje (szybszy - streaming).",
            "DNS: Tłumaczy nazwy (google.pl) na IP.",
            "DHCP: Przydziela automatycznie adresy IP."
        ]),
        ("GRAFIKA I MiTI", [
            "RGB: Monitor (addytywny). CMYK: Druk (substraktywny).",
            "Kompresja: Stratna (JPG - tracisz detale), Bezstratna (PNG, ZIP).",
            "Histogram: Wykres jasności pikseli. Wyrównanie poprawia kontrast.",
            "WCAG: Standardy dostępności stron (np. dla niewidomych)."
        ]),
        ("PROGRAMOWANIE (OOP)", [
            "Klasa: Szablon/Foremka. Obiekt: Konkretny byt utworzony z klasy.",
            "Hermetyzacja: Ukrywanie danych (private) i wystawianie metod (public).",
            "Dziedziczenie: Przejmowanie cech klasy nadrzędnej.",
            "Polimorfizm: Ta sama metoda działa różnie dla różnych obiektów."
        ])
    ]

    for section, items in cheat_sheet:
        elements.append(Paragraph(section, h1_style))
        for item in items:
            elements.append(Paragraph(f"• {item}", bullet_style))
        elements.append(Spacer(1, 5))

    doc.build(elements)

create_study_plan_pdf("Plan_Nauki_Inzynier_UKEN.pdf")