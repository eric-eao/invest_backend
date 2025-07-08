[Movimento novo (PENDING)] 
       ↓
create_movement()
       ↓
[Movimento salvo com status = PENDING]
       ↓
update_asset_position()        → atualiza quantidade e custo médio no asset
       ↓
process_positions_service()
       ↓
  ├── busca movimentos PENDING
  ├── remove positions apenas desses movimentos
  ├── aplica FIFO e recria os lotes
  └── marca movimentos processados como CONFIRMED
       ↓
positions atualizada
       ↓
pronto para marcação a mercado

-----------------------------------------------------------

[Movimento editado]
       ↓
update_movement()
       ↓
marca status = PENDING
       ↓
update_asset_position()
       ↓
process_positions_service()
       ↓
  ├── busca movimentos PENDING
  └── reconstrói apenas posições afetadas
       ↓
positions atualizada

-----------------------------------------------------------

[Movimento excluído]
       ↓
delete_movement()
       ↓
marca status = PENDING apenas para movimentos do mesmo asset
       ↓
update_asset_position()
       ↓
process_positions_service()
       ↓
  ├── remove positions apenas do asset afetado
  └── reconstrói apenas o asset envolvido
       ↓
positions atualizada
