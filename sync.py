import functools

async def sync_bloqueante(cliente, funcion, *args):
  if cliente is None:
    return funcion(*args)
  return await cliente.loop.run_in_executor(None, functools.partial(funcion, *args))