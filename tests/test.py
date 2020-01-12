import panaetius

# from panaetius import CONFIG as CONFIG
# from panaetius import logger as logger

print(panaetius.__header__)

panaetius.set_config(panaetius.CONFIG, 'logging.level')

# print(panaetius.CONFIG.logging_format)
print(panaetius.CONFIG.logging_path)
print(panaetius.config_inst.CONFIG_PATH)

# panaetius.logger.info('test event')


panaetius.logger.info('setting foo.bar value')
panaetius.set_config(panaetius.CONFIG, 'foo.bar', mask=True)

panaetius.logger.info(f'foo.bar set to {panaetius.CONFIG.foo_bar}')

# print((panaetius.CONFIG.path))
# print(panaetius.CONFIG.logging_level)

panaetius.set_config(panaetius.CONFIG, 'test', mask=True)
panaetius.logger.info(f'test_root={panaetius.CONFIG.test}')

print(panaetius.CONFIG.config_file)

# for i in panaetius.CONFIG.deferred_messages:
#     panaetius.logger.debug(i)
