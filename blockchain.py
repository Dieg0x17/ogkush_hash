import secrets
import json
import time
import ogkush

def hashf(value):
    return ogkush.ogkush(value)


def gen_block(pre_block, value):
    print("Generando bloque ", value, '\n'+pre_block)
    to = time.time()
    pre_sign = hashf(pre_block)
    # solucionando el problema
    solution = "***"
    while solution[:2] != "00":   
        problem = secrets.token_bytes(64).hex()
        block = problem +'\n'+ value +'\n'+ pre_sign +'\n'+str(to)+'\n'

        sign = hashf(block)
        signed_block = block+sign+'\n'

        solution = hashf(signed_block)
        tf = time.time()
        # pensar en meter el numero de bloque y el timestamp para facil orden

    deltat = tf-to
    print("solucion encontrada en", deltat, "s", solution)
    return signed_block


def check_block(pre_block, block):
    solution = hashf(block)
    # se comprueba si esta resuelto
    if solution[:2] == "00":
        deserialize = block.split('\n')
        # obtener el valor   
        problem = deserialize[0]
        value = deserialize[1]
        pre =   deserialize[2] 
        # se comprueba la cadena
        if pre == hashf(pre_block):
            # se comprueba la integridad del bloque
            time = deserialize[3] 
            integrity = deserialize[4] 
            if integrity == hashf(problem +'\n'+ value +'\n'+ pre +'\n'+time +'\n'):
                return value
    return "Format error"


def mine(nombre, value):
    reg = open(nombre, "r")
    ds = json.loads(reg.read())
    # obtener ultimo bloque
    last_block = ds[len(ds)-1]
    # generar bloque
    block = gen_block(last_block, value)
    ds.append(block)
    data = json.dumps(ds)
    reg = open(nombre, "w")
    reg.write(data)


def get_values(nombre):
    reg = open(nombre, "r")
    ds = json.loads(reg.read())
    reg.close()
    # omitimos el bloque genesis
    values = []
    for i in range(len(ds)-1):
        pre = ds[i]
        curr = ds[i+1]
        val = check_block(pre, curr)
        if val != "Format error":
            values.append(val)
        else:
            return "Structural damage"
    return values


def start_blockchain(nombre, value):
    ds = []
    genesis = gen_block("00", value)
    ds.append(genesis)
    data = json.dumps(ds)
    reg = open(nombre, "w")
    reg.write(data)


nombre = "00chain_data"
if __name__ == "__main__":
    start_blockchain(nombre, "bloque_primigeneo")
    for i in range(3):
        mine(nombre, str(i)+"000 > iduser")
    print(get_values(nombre))
