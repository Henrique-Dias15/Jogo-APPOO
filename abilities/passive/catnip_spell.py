from abilities.base_ability import PassiveAbility

class CatnipSpell(PassiveAbility):
    """Feitiço de Catnip - Aumenta o poder mágico"""
    def __init__(self):
        super().__init__(
            name="Feitiço de Catnip",
            description="Aumenta o poder mágico permanentemente",
            stat_name="projectile_damage",
            stat_increase=5
        )
