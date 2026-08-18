package com.tekoaly.nappaimisto

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun NappaimistoUi(
    ehdotettuSana: String,
    onKirjainPainettu: (String) -> Unit,
    onEhdotusValittu: (String) -> Unit
) {
    // Teeman värit: syvä tumma tausta, keltainen tekoälytehoste
    val tausta = Color(0xFF121212)
    val nappainVari = Color(0xFF222222)
    val tekstiVari = Color(0xFFFFFFFF)
    val korostusVari = Color(0xFFFFD700)

    Column(
        modifier = Modifier
            .fillMaxWidth()
            .background(tausta)
            .padding(bottom = 8.dp)
    ) {
        // 1. TEKOÄLYN ENNAKOIVA PALKKI
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .height(45.dp)
                .background(Color(0xFF1C1C1C)),
            horizontalArrangement = Arrangement.Center,
            verticalAlignment = Alignment.CenterVertically
        ) {
            if (ehdotettuSana.isNotEmpty()) {
                Text(
                    text = ehdotettuSana,
                    color = korostusVari,
                    fontSize = 18.sp,
                    modifier = Modifier
                        .padding(horizontal = 16.dp, vertical = 4.dp)
                        .clickable { onEhdotusValittu(ehdotettuSana) }
                )
            }
        }

        Spacer(modifier = Modifier.height(8.dp))

        // 2. NÄPPÄIMISTÖN RIVIT (Esimerkkinä ylin QWERTY-rivi)
        val ylinRivi = listOf("Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P")
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceEvenly
        ) {
            for (kirjain in ylinRivi) {
                Button(
                    onClick = { onKirjainPainettu(kirjain) },
                    colors = ButtonDefaults.buttonColors(containerColor = nappainVari),
                    contentPadding = PaddingValues(0.dp),
                    modifier = Modifier
                        .weight(1f)
                        .padding(2.dp)
                        .height(50.dp)
                ) {
                    Text(text = kirjain, color = tekstiVari, fontSize = 16.sp)
                }
            }
        }
    }
}
