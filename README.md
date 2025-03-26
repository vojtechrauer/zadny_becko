Webová aplikace **Žádný Béčko** slouží ke sdílení filmových recenzí. Back-end je napsaný v Python frameworku Django dle architektury MVT a využívá vestavěnné ORM funkcionality. Nadefinované je množství modelů a funkcionálních views, které obsluhují potřebné uživatelské akce a CRUD operace. Aplikace rozlišuje dva typy uživatelů, běžného a admina, z nichž administrátor může upravovat, přidávat a mazat veškerý uživatelsky vytvořený obsah aplikace. Pro přívětivější UI jsou nadefinovány možnosti přidání obrázků k hlavním entitám v databázi. Stránka se seznamy recenzí a filmů umožňuje vyhledávání v nadpisech entit. Jednotlivé modely jsou na sebe napojeny v databázi, tudíž aplikace umožňuje zobrazení instancí, které spolu souvisejí (například recenzí u určitého filmu, filmů u režiséra, popř. recenze napsané uživatelem a jeho oblíbené filmy).

