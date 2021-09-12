""" tests.test_cli """
import logging


logger = logging.getLogger(__name__)


def test_seed_user(runner):
    result_up = runner.invoke(args=["seed", "user", "up"])
    result_down = runner.invoke(args=["seed", "user", "down"])
    logger.info(str(result_up))
    logger.info(str(result_down))
    assert result_up.exit_code == 0 and result_down.exit_code == 0


def test_seed_admin(runner):
    result_up = runner.invoke(args=["seed", "admin", "up"])
    result_down = runner.invoke(args=["seed", "admin", "down"])
    logger.info(result_up)
    logger.info(result_down)
    assert result_up.exit_code == 0 and result_down.exit_code == 0
