from cpu.pipeline import Pipeline
from cpu.isa import procesar_con_etiquetas

def cargar_programa(path):
    with open(path, "r") as f:
        lines = f.readlines()
    return procesar_con_etiquetas(lines)

def main():
    pipeline = Pipeline()
    instrucciones, etiquetas = cargar_programa("tests/benchmark4.txt")
    pipeline.load_program((instrucciones, etiquetas))

    pipeline.cache.write(0, 10)
    pipeline.cache.write(4, 20)

    while any([pipeline.IF.instr, pipeline.ID.instr, pipeline.EX.instr,
               pipeline.MEM.instr, pipeline.WB.instr]) or pipeline.pc < len(instrucciones):
        pipeline.cycle()

    print("\n--- Registro R3 ---")
    print(f"R3 = {pipeline.registers['R3']}")

if __name__ == "__main__":
    main()
