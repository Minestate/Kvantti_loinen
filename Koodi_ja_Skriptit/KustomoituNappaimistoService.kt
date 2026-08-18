package com.tekoaly.nappaimisto

import android.inputmethodservice.InputMethodService
import android.view.View
import androidx.compose.runtime.*
import androidx.compose.ui.platform.ComposeView

class KustomoituNappaimistoService : InputMethodService() {

    private val ennustaja = OfflineEnnustaja()
    private var dynaaminenEhdotus by mutableStateOf("")

    override fun onCreateInputView(): View {
        return ComposeView(this).apply {
            setContent {
                NappaimistoUi(
                    ehdotettuSana = dynaaminenEhdotus,
                    onKirjainPainettu = { kirjain ->
                        kasitteleKirjainPainallus(kirjain)
                    },
                    onEhdotusValittu = { sana ->
                        kasitteleEnnusteenValinta(sana)
                    }
                )
            }
        }
    }

    private fun kasitteleKirjainPainallus(kirjain: String) {
        val ic = currentInputConnection ?: return
        
        // Lähetetään merkki aktiiviseen sovellukseen
        ic.commitText(kirjain, 1)
        
        // Päivitetään tekoälyn ennustus
        paivitaEnnustus()
    }

    private fun paivitaEnnustus() {
        val ic = currentInputConnection ?: return
        
        // Haetaan maksimissaan 50 merkkiä kursoria ennen olevaa tekstiä kontekstiksi
        val tekstiEnnen Kursorria = ic.getTextBeforeCursor(50, 0)
        
        if (!tekstiEnnen.isNullString() && tekstiEnnen.isNotEmpty()) {
            val sanat = tekstiEnnen.toString().trim().split(" ")
            val viimeisinSana = sanat.last()

            // Kysytään tekoälyltä offline-ennustetta
            val ennuste = ennustaja.haeSeuraavaSana(viimeisinSana)
            dynaaminenEhdotus = ennuste ?: ""
        } else {
            dynaaminenEhdotus = ""
        }
    }

    private fun kasitteleEnnusteenValinta(sana: String) {
        val ic = currentInputConnection ?: return
        
        // Lisätään ennustettu sana ja välilyönti tekstikenttään
        ic.commitText("$sana ", 1)
        
        // Tyhjennetään ehdotuspalkki valinnan jälkeen
        dynaaminenEhdotus = ""
    }
}

// Apulaajennus tyhjän tekstin tarkistukseen
fun CharSequence?.isNullString(): Boolean = this == null
