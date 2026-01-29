

## [1.2.0] - 2026-01-29

### 🚀 Major Update - Scraper Intelligente

#### Fixed
- **Canali TV errati**: Serie A distingue correttamente DAZN vs DAZN+Sky
- **Serie B sempre corretta**: DAZN, LaB Channel (Prime Video)
- **Partite mancanti**: Aggiunto sistema eventi manuali

#### Added
- Riconoscimento intelligente canali per competizione
- Mapping canali TV automatico (Serie A, B, Champions, ecc.)
- Funzione `add_manual_events()` per integrare partite mancanti
- Helper script `helper_add_events.py` per aggiunta rapida
- Guida manutenzione settimanale completa
- Template eventi manuali configurabili

#### Improved
- Logica Serie A: verifica testo per distinguere DAZN/Sky
- Parsing competizioni più accurato (riconosce giornata)
- Prevenzione duplicati con similarità eventi
- Estrazione note migliorata (Diretta Gol, Semifinali, ecc.)

#### Documentation
- `GUIDA_MANUTENZIONE.md`: workflow settimanale
- `NOTE_CANALI_TV.md`: regole diritti TV
- `EVENTI_MANUALI.txt`: template configurazione
- `RIEPILOGO_FINALE_v1.2.md`: panoramica completa

---
