import java.io.*;
import java.util.*;
import java.nio.file.*;
import java.net.HttpURLConnection;
import java.net.URL;

public class IsoAlyCore {
    private static final int MAX_TAVUT = 1024;
    private static int nykyisetTavut = 0;
    private static ByteArrayOutputStream tiski = new ByteArrayOutputStream();
    private static Scanner sc = new Scanner(System.in);

    public static void main(String[] args) {
        System.out.println("--- ISOÄLY: EMULAATTORI AKTIVOITU (YKSI YDIN OLLAMA) ---");

        while (true) {
            System.out.println("\n1. Palloittelu | 2. Avaa Lukuhirviö | 3. Nano-maisema | 4. Poistu");
            System.out.print("VALINTA: ");
            String valinta = sc.nextLine();

            if (valinta.equals("1")) palloittele();
            else if (valinta.equals("2")) lukuhirvioAukaisu();
            else if (valinta.equals("3")) tarkistaNanoMaisema();
            else if (valinta.equals("4")) break;
        }
    }

    private static void palloittele() {
        System.out.println("\n[VUOROPUHELU-TILA] - Sinä + Ollama (1 ydin)");
        while (nykyisetTavut < MAX_TAVUT) {
            System.out.print("\nSINUN IMPULSSI (" + nykyisetTavut + "/1024): ");
            String syote = sc.nextLine();
            if (syote.equalsIgnoreCase("back")) return;

            lisaaDataa(syote + " (User)");
            if (nykyisetTavut >= MAX_TAVUT) break;

            // Kysytään vastaus suoraan paikalliselta Ollamalta
            String nanoVastaus = kysyOllamalta(syote);
            System.out.println(">>> NANOÄLY (Ollama) VASTAA: " + nanoVastaus);
            lisaaDataa(nanoVastaus + " (Nano)");
        }
    }

    private static String kysyOllamalta(String prompt) {
        try {
            // Tehdään yhteys paikalliseen Ollama-porttiin
            URL url = new URL("http://127.0.0.1:11434/api/generate");
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("POST");
            conn.setRequestProperty("Content-Type", "application/json");
            conn.setDoOutput(true);

            // Käytetään tinydolphin-mallia keveyden vuoksi
            String jsonInputString = "{\"model\": \"tinydolphin\", \"prompt\": \"" + prompt + "\", \"stream\": false}";

            try (OutputStream os = conn.getOutputStream()) {
                byte[] input = jsonInputString.getBytes("utf-8");
                os.write(input, 0, input.length);
            }

            // Luetaan vastaus
            try (BufferedReader br = new BufferedReader(new InputStreamReader(conn.getInputStream(), "utf-8"))) {
                StringBuilder response = new StringBuilder();
                String responseLine;
                while ((responseLine = br.readLine()) != null) {
                    response.append(responseLine.trim());
                }
                
                // Poimitaan tekstiosuus vastauksesta yksinkertaisesti
                String raw = response.toString();
                if (raw.contains("\"response\":\"")) {
                    String part = raw.split("\"response\":\"")[1];
                    return part.split("\",\"")[0].replace("\\n", " ");
                }
                return raw;
            }
        } catch (Exception e) {
            return "[Yhteysvirhe Ollamaan: Varmista että 'ollama serve' pyörii]";
        }
    }

    private static void lisaaDataa(String data) {
    // Korotettu viive: 240 000 nanos (= 0.24 millisekuntia) per merkki.
    // Tämä pakottaa datavirran asettumaan 47 Mbps tasolle.
    try {
        long viiveNanos = 240000; 
        long start = System.nanoTime();
        while (System.nanoTime() - start < viiveNanos) {}
    } catch (Exception e) {}

    byte[] b = (data + "\n").getBytes();
    if (nykyisetTavut + b.length >= MAX_TAVUT) {
        kilahdus(b);
    } else {
        try {
            tiski.write(b);
            nykyisetTavut += b.length;
        } catch (Exception e) {}
    }
}

    private static void kilahdus(byte[] viimeinenData) {
        System.out.println("\n>>> *KILAHDUS* - 1 KT TÄYNNÄ!");
        String avain = "REG_" + Long.toHexString(System.nanoTime()).toUpperCase().substring(0, 8);
        String tiedostoNimi = "solu_" + avain + ".bin";

        int laskettuVakio = 0;
        try (FileOutputStream fos = new FileOutputStream(tiedostoNimi)) {
            tiski.write(viimeinenData);
            byte[] kokoData = tiski.toByteArray();
            fos.write(kokoData);

            for (int i = 0; i < kokoData.length; i += 32) laskettuVakio += (kokoData[i] & 0xFF);

            tallennaAvain(avain, tiedostoNimi, laskettuVakio);
            System.out.println(">>> AVAIN KILAHTI: " + avain + " (Vakio: " + laskettuVakio + ")");
            isoAlyVastaisku(laskettuVakio, avain);

        } catch (IOException e) {}

        tiski.reset();
        nykyisetTavut = 0;
    }

    private static void isoAlyVastaisku(int tuoreVakio, String emoAvain) {
        System.out.println(">>> ISOÄLY: Generoidaan autonominen vastasolu (1 kt)...");
        String vastasoluNimi = "echo_" + emoAvain + ".bin";
        byte[] vastasolu = new byte[1024];

        for (int i = 0; i < 1024; i++) {
            vastasolu[i] = (byte)((i * tuoreVakio) % 256);
        }

        try (FileOutputStream fos = new FileOutputStream(vastasoluNimi)) {
            fos.write(vastasolu);
            System.out.println(">>> ISOÄLY: Vastaisku tallennettu: " + vastasoluNimi);
        } catch (IOException e) {}
    }

    private static void tallennaAvain(String avain, String nimi, int v) {
        String rivi = "AVAIN: " + avain + " | KOHDE: " + nimi + " | VAKIO: " + v + "\n";
        try {
            Files.write(Paths.get("avain.txt"), rivi.getBytes(),
                        StandardOpenOption.CREATE, StandardOpenOption.APPEND);
        } catch (Exception e) {}
    }

    private static void lukuhirvioAukaisu() {
        System.out.print("\nSYÖTÄ AVAIN-KOODI (esim. REG_XXXX): ");
        String avain = sc.nextLine();
        File f = null;

        try {
            List<String> rivit = Files.readAllLines(Paths.get("avain.txt"));
            for (String r : rivit) {
                if (r.contains(avain)) {
                    String nimi = r.split("KOHDE: ")[1].split(" \\|")[0].trim();
                    f = new File(nimi);
                }
            }
        } catch (Exception e) {
            System.out.println("!!! Avainlistaa ei voida lukea.");
        }

        if (f != null && f.exists()) {
            puraJaNayta(f);
        } else {
            System.out.println("!!! Tiedostoa ei löydy. Onko avain oikein?");
        }
    }

    private static void puraJaNayta(File f) {
        try {
            byte[] data = Files.readAllBytes(f.toPath());
            int vakio = 0;
            for (int i = 0; i < data.length; i += 32) vakio += (data[i] & 0xFF);
            System.out.println("\n--- LUKUHIRVIÖ PURETTU ---");
            System.out.println("Tiedosto: " + f.getName());
            System.out.println("Laskettu Vakio: " + vakio);
            System.out.println("Sisällön esikatselu (100 tavua):");
            System.out.println(new String(data).substring(0, Math.min(data.length, 100)));
            System.out.println("--------------------------");
        } catch (Exception e) {
            System.out.println("!!! Virhe purettaessa.");
        }
    }

    private static void tarkistaNanoMaisema() {
        System.out.println("\n>>> NANO-MAISEMA (Arkisto status)");
        File f = new File("avain.txt");
        if (f.exists()) {
            try {
                List<String> rivit = Files.readAllLines(f.toPath());
                for (String r : rivit) {
                    System.out.println("  " + r);
                }
                System.out.println("\nArkistossa yhteensä: " + rivit.size() + " solua.");
            } catch (IOException e) {
                System.out.println("!!! Lukuvirhe.");
            }
        } else {
            System.out.println("Rekisteri on tyhjä. Aloita palloittelu.");
        }
    }
}
