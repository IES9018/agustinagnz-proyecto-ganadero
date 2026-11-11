DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM animales
        WHERE sexo IS NULL OR BTRIM(sexo) = ''
    ) THEN
        RAISE EXCEPTION
            'No se puede establecer NOT NULL: existen animales sin sexo informado.';
    END IF;
END
$$;

ALTER TABLE animales
ALTER COLUMN sexo SET NOT NULL;