BEGIN;

ALTER TABLE stock_insumos
ADD COLUMN IF NOT EXISTS stock_minimo FLOAT;

UPDATE stock_insumos
SET stock_minimo = COALESCE(stock_minimo, 10);

ALTER TABLE stock_insumos
ALTER COLUMN stock_minimo SET DEFAULT 10;

ALTER TABLE stock_insumos
ALTER COLUMN stock_minimo SET NOT NULL;

ALTER TABLE stock_insumos
DROP COLUMN IF EXISTS stock_critico;

COMMIT;