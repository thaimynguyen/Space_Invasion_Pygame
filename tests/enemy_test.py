import pytest
from settings import Settings
from player import PlayerShip, PlayerBullet
from enemy import EnemyShip, EnemyBullet


@pytest.fixture(scope="function")
def settings() -> Settings:
    return Settings()


@pytest.fixture(scope="function")
def player_bullet(settings: Settings) -> PlayerBullet:
    return PlayerBullet(50, 50, settings)


@pytest.fixture(scope="function")
def player_ship(settings: Settings) -> PlayerShip:
    return PlayerShip(settings)


@pytest.fixture(scope="function")
def enemy_ship(settings: Settings) -> EnemyShip:
    return EnemyShip(settings)


@pytest.fixture(scope="function")
def enemy_bullet(settings: Settings) -> EnemyBullet:
    return EnemyBullet(50, 50, settings)


"""
Test on EnemyShip
"""


def test_enemy_ship_update(enemy_ship: EnemyShip):
    enemy_ship.x = 100
    enemy_ship.y = 100
    enemy_ship.update()
    assert enemy_ship.x == 100
    assert enemy_ship.y == 102


def test_enemy_ship_shoot(enemy_ship: EnemyShip):
    enemy_ship.x = 100
    enemy_ship.y = 100
    bullet = enemy_ship.shoot()
    assert isinstance(bullet, EnemyBullet)
    assert bullet.x == enemy_ship.x
    assert bullet.y == enemy_ship.y + 10


def test_enemy_ship_on_collision_with_player_ship(
    enemy_ship: EnemyShip, player_ship: PlayerShip
):
    enemy_ship.on_collision(player_ship)
    assert enemy_ship.should_be_removed


def test_enemy_ship_on_collision_with_player_bullet(
    enemy_ship: EnemyShip, player_bullet: PlayerBullet
):
    enemy_ship.on_collision(player_bullet)
    assert enemy_ship.should_be_removed


def test_enemy_ship_on_collision_with_enemy_bullet(
    enemy_ship: EnemyShip, enemy_bullet: EnemyBullet
):
    enemy_ship.on_collision(enemy_bullet)
    assert enemy_ship.should_be_removed is False


"""
Test on EnemyBullet
"""


def test_enemy_bullet_update(enemy_bullet: EnemyBullet):
    enemy_bullet.x = 100
    enemy_bullet.y = 100
    enemy_bullet.update()
    assert enemy_bullet.x == 100
    assert enemy_bullet.y == 110


def test_enemy_bullet_on_collision_with_player_ship(
    enemy_bullet: EnemyBullet, player_ship: PlayerShip
):
    enemy_bullet.on_collision(player_ship)
    assert enemy_bullet.should_be_removed
