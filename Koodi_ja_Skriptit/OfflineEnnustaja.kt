package com.tekoaly.nappaimisto

class OfflineEnnustaja {
    // Paikallinen välimuisti sanojen suhteille: { "nykyinen_sana" : { "seuraava_sana" : painokerroin } }
    private val ennustusMatrix = HashMap<String, HashMap<String, Int>>()

    init {
        // Esiopetetaan järjestelmään ydinrakenteet suoraan muistiin offline-alustusta varten
        opetaLause("tutkielman tila on dokumentoitu ja suljettu")
        opetaLause("perusta base on järjestelmän ydin")
        opetaLause("kaikki tiedot on vakuutettu ja säilötty muistiin")
    }

    fun opetaLause(lause: String) {
        val sanat = lause.lowercase().replace(Regex("[^a-zåäö ]"), "").split(" ")
        if (sanat.size < 2) return

        for (i in 0 until sanat.size - 1) {
            val nykyinen = sanat[i]
            val seuraava = sanat[i + 1]

            if (nykyinen.isEmpty() || seuraava.isEmpty()) continue

            if (!ennustusMatrix.containsKey(nykyinen)) {
                ennustusMatrix[nykyinen] = HashMap()
            }
            val siirtymat = ennustusMatrix[nykyinen]!!
            siirtymat[seuraava] = (siirtymat[seuraava] ?: 0) + 1
        }
    }

    fun haeSeuraavaSana(viimeisinSana: String): String? {
        val puhdasSana = viimeisinSana.lowercase().trim()
        val siirtymat = ennustusMatrix[puhdasSana] ?: return null

        // Haetaan siirtymistä se sana, jolla on suurin painokerroin (todennäköisyys)
        return siirtymat.maxByOrNull { it.value }?.key
    }
}
