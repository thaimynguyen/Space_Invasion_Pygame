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
Test on PlayerShip
"""


def test_player_ship_update(player_ship: PlayerShip):
    player_ship._invulnerable_frame = 10
    player_ship.update()
    assert player_ship._invulnerable_frame == 9


def test_player_ship_move_left(player_ship: PlayerShip):
    player_ship.x, player_ship.y = 100, 100
    player_ship.move_left()
    assert player_ship.x == 95
    assert player_ship.y == 100


def test_player_ship_move_right(player_ship: PlayerShip):
    player_ship.x, player_ship.y = 100, 100
    player_ship.move_right()
    assert player_ship.x == 105
    assert player_ship.y == 100


def test_player_ship_shoot(player_ship: PlayerShip):
    bullet = player_ship.shoot()
    assert isinstance(bullet, PlayerBullet)


def test_player_ship_on_collision_with_enemy_ship(
    player_ship: PlayerShip, enemy_ship: EnemyShip
):
    player_ship._invulnerable_frame = 0
    player_ship.on_collision(enemy_ship)
    assert player_ship.should_be_removed is True


def test_player_ship_on_collision_with_enemy_bullet(
    player_ship: PlayerShip, enemy_bullet: EnemyBullet
):
    player_ship._invulnerable_frame = 0
    player_ship.on_collision(enemy_bullet)
    assert player_ship.should_be_removed is True


"""
Test on PlayerBullet
"""


def test_player_bullet_update(player_bullet: PlayerBullet):
    player_bullet.update()
    assert player_bullet.x == 50
    assert player_bullet.y == 40


def test_player_bullet_on_collision_with_enemy_ship(
    player_bullet: PlayerBullet, enemy_ship: EnemyShip
):
    player_bullet.on_collision(enemy_ship)
    assert player_bullet.should_be_removed
