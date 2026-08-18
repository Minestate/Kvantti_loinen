import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.web.WebView;
import javafx.stage.Stage;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.charset.StandardCharsets;

public class PerustaBrowser extends Application {

    // --- 1. KILOTAVUEDITORI-LOGIIKKA ---
    public static class KilotavuEditori {
        private final String[] akkutiedostot = {"par_1.dat", "par_2.dat", "par_3.dat"};
        private final int tavuRaja = 1024;

        public double mittaaRamKapasiteetti() {
            // Luetaan järjestelmän fyysinen RAM Runtime-ympäristöstä tai OS-rajapinnasta
            long muistiTavuina = ((com.sun.management.OperatingSystemMXBean) 
                java.lang.management.ManagementFactory.getOperatingSystemMXBean())
                .getTotalMemorySize();
            return (double) muistiTavuina / (1024 * 1024 * 1024);
        }

        public void tallennaTila(int kk, double sisaan, double ulos, double saldo, String profiili) {
            String lokidata = String.format("SYKLI_KK:%02d|IN:%.2f|OUT:%.2f|BAL:%.2f|PROF:%s\n", 
                    kk, sisaan, ulos, saldo, profiili);
            String lohkoSisalto = "AKKU_LUKITUS_LOGISET_JÄLJET\n" + lokidata;
            byte[] dataBytes = lohkoSisalto.getBytes(StandardCharsets.UTF_8);

            // Pakotetaan tasan 1024 tavun puskuri (Mekaaninen vakaus)
            byte[] paddattuData = new byte[tavuRaja];
            System.arraycopy(dataBytes, 0, paddattuData, 0, Math.min(dataBytes.length, tavuRaja));

            for (String tiedosto : akkutiedostot) {
                try (FileOutputStream fos = new FileOutputStream(new File(tiedosto))) {
                    fos.write(paddattuData);
                } catch (IOException e) {
                    System.err.println("[Virhe] Akkulukitus epäonnistui: " + e.getMessage());
                }
            }
        }
    }

    // --- 2. MC-1 MOBIILI-CONTROLLER ---
    public static class MobiiliControllerMC1 {
        public String nykyinenProfiili = "Alustamaton";
        public String cpuTaajuus = "Normaali";

        public boolean asetaProfiili(double ramGb) {
            if (ramGb < 8.0) {
                this.nykyinenProfiili = "SULJETTU (Matala RAM)";
                this.cpuTaajuus = "Powersave";
                return false;
            } else if (ramGb < 12.0) {
                this.nykyinenProfiili = "Ghost";
                this.cpuTaajuus = "Minimi (Säästö)";
            } else if (ramGb <= 16.0) {
                this.nykyinenProfiili = "Eco";
                this.cpuTaajuus = "Balansoidut taajuudet";
            } else {
                this.nykyinenProfiili = "Turbo";
                this.cpuTaajuus = "Maksimaaliset taajuudet";
            }
            return true;
        }
    }

    // --- 3. BROWSER & SIMULAATIOAJURI ---
    @Override
    public void start(Stage primaryStage) {
        WebView webView = new WebView();
        
        // Alustetaan Perusta-komponentit
        KilotavuEditori editori = new KilotavuEditori();
        MobiiliControllerMC1 mc1 = new MobiiliControllerMC1();
        
        double mitattuRam = editori.mittaaRamKapasiteetti();
        boolean ajokelpoinen = mc1.asetaProfiili(mitattuRam);

        // Generoidaan selainnäkymän HTML-sisältö dynaamisesti
        StringBuilder html = new StringBuilder();
        html.append("<html><head><style>")
            .append("body { font-family: monospace; background-color: #0d1117; color: #c9d1d9; padding: 20px; }")
            .append("h1 { color: #58a6ff; border-bottom: 1px solid #30363d; padding-bottom: 10px; }")
            .append(".status-box { background-color: #161b22; padding: 15px; border-radius: 5px; border: 1px solid #30363d; margin-bottom: 20px; }")
            .append(".turbo { color: #238636; font-weight: bold; }")
            .append(".ghost { color: #d29922; font-weight: bold; }")
            .append("table { width: 100%; border-collapse: collapse; margin-top: 20px; }")
            .append("th, td { text-align: left; padding: 8px; border-bottom: 1px solid #21262d; }")
            .append("th { background-color: #161b22; color: #58a6ff; }")
            .append(".success { color: #56d364; font-weight: bold; }")
            .append("</style></head><body>");

        html.append("<h1>PERUSTA - JÄRJESTELMÄN KOKONAISARKKITEHTUURI</h1>");
        html.append("<div class='status-box'>");
        html.append("<strong>KilotavuEditori RAM-mittaus:</strong> ").append(String.format("%.2f GB RAM", mitattuRam)).append("<br>");
        html.append("<strong>MC-1 Profiili:</strong> <span class='turbo'>").append(mc1.nykyinenProfiili).append("</span> (").append(mc1.cpuTaajuus).append(")<br>");
        html.append("</div>");

        if (!ajokelpoinen) {
            html.append("<h2 style='color:#f85149;'>KRIITTINEN VIRHE: Järjestelmä vaatii vähintään 8 GB RAM-muistia.</h2></body></html>");
            webView.getEngine().loadContent(html.toString());
            asetuksetJaNaytto(primaryStage, webView);
            return;
        }

        // Suoritetaan 36 kk talouskierto
        long osallistujat = 2200000;
        double kuukausimaksu = 138.95;
        double palautusSumma = 555.55;
        int kestoKk = 36;
        int palautusErat = 9;
        int palautusAlkaaKk = kestoKk - palautusErat + 1;

        double kassavirtaSisaan = 0.0;
        double kassavirtaUlos = 0.0;

        html.append("<h3>Syklin mekaaninen ajoloki (36 kk)</h3>");
        html.append("<table><tr><th>Kuukausi</th><th>Sisäänvirtaus (M€)</th><th>Ulosvirtaus (M€)</th><th>Järjestelmän Saldo (€)</th></tr>");

        for (int kk = 1; kk <= kestoKk; kk++) {
            kassavirtaSisaan += osallistujat * kuukausimaksu;
            
            double kuukausiUlos = 0.0;
            if (kk >= palautusAlkaaKk) {
                kuukausiUlos = osallistujat * palautusSumma;
                kassavirtaUlos += kuukausiUlos;
            }

            double nykyinenSaldo = kassavirtaSisaan - kassavirtaUlos;

            // Lukitaan tila taustalla tasan 1024 tavun akkuihin
            editori.tallennaTila(kk, kassavirtaSisaan, kassavirtaUlos, nykyinenSaldo, mc1.nykyinenProfiili);

            // Tulostetaan selaimeen kriittiset pisteet vähentämään visuaalista kuormaa
            if (kk == 1 || kk == palautusAlkaaKk || kk == kestoKk) {
                html.append(String.format("<tr><td>KK %02d</td><td>%,.2f</td><td>%,.2f</td><td><strong>%,.2f €</strong></td></tr>", 
                        kk, kassavirtaSisaan / 1000000, kassavirtaUlos / 1000000, nykyinenSaldo));
            }
        }

        html.append("</table>");

        // Lopputuloksen vahvistus nollatilatavoitteesta
        double loppusaldo = kassavirtaSisaan - kassavirtaUlos;
        html.append("<br><div class='status-box'>");
        html.append("<h3>SÝKLIN LOPPURAPORTTI</h3>");
        html.append("Kokonaiskertymä (In): ").append(String.format("%,.2f €", kassavirtaSisaan)).append("<br>");
        html.append("Kokonaispalautus (Out): ").append(String.format("%,.2f €", kassavirtaUlos)).append("<br>");
        html.append("Järjestelmän jäännössaldo: <strong>").append(String.format("%,.2f €", loppusaldo)).append("</strong><br><br>");

        if (Math.abs(loppusaldo - 4950000.00) < 0.01) {
            html.append("<span class='success'>> TILA: MATEMAATTINEN TASAPAINO LUKITTU (4,950,000.00 €) <</span><br>");
            html.append("> MC-1 ohjain siirtänyt laitteiston ylläpitotilaun. Järjestelmä stabiili.");
        }
        html.append("</div></body></html>");

        // Ladataan luotu HTML suoraan selaimeen
        webView.getEngine().loadContent(html.toString());
        asetuksetJaNaytto(primaryStage, webView);
    }

    private void asetuksetJaNaytto(Stage stage, WebView webView) {
        Scene scene = new Scene(webView, 900, 650);
        stage.setTitle("Perusta Arkkitehtuuri - KilotavuEditori & MC-1 Selain");
        stage.setScene(scene);
        stage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }
}