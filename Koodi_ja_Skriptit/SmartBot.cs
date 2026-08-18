using CounterStrikeSharp.API;
using CounterStrikeSharp.API.Core;
using CounterStrikeSharp.API.Modules.Utils;

namespace CS2SmartBot;

public enum BotState
{
    Patrol,
    Engage,
    Reload
}

public class CS2SmartBotPlugin : BasePlugin
{
    public override string ModuleName => "CS2 Smart Bot";
    public override string ModuleVersion => "1.0.0";

    public override void Load(bool hotReload)
    {
        RegisterListener<Listeners.OnTick>(OnServerTick);
    }

    private void OnServerTick()
    {
        var bots = Utilities.GetPlayers().Where(p => p.IsBot && p.PawnIsAlive);

        foreach (var bot in bots)
        {
            var controller = new AdvancedBotController(bot);
            controller.UpdateLogic();
        }
    }
}

public class AdvancedBotController
{
    private CCSPlayerController _bot;
    private BotState _currentState = BotState.Patrol;
    private static DateTime _lastTargetSeen = DateTime.MinValue;
    private static int _shotsFired = 0;

    public AdvancedBotController(CCSPlayerController bot)
    {
        _bot = bot;
    }

    public void UpdateLogic()
    {
        var pawn = _bot.PlayerPawn.Value;
        if (pawn == null || !pawn.IsValid || pawn.Health <= 0) return;

        var target = FindNearestEnemy();

        if (target != null && target.PlayerPawn.Value != null)
        {
            var targetPawn = target.PlayerPawn.Value;
            Vector botPos = pawn.AbsOrigin ?? new Vector(0, 0, 0);
            Vector enemyPos = targetPawn.AbsOrigin ?? new Vector(0, 0, 0);

            _currentState = BotState.Engage;
            _lastTargetSeen = DateTime.Now;

            AimAndShoot(pawn, botPos, enemyPos);
        }
        else
        {
            _currentState = BotState.Patrol;
            _shotsFired = 0;
        }

        // Käytetään tilaa, jotta kääntäjä ei anna CS0414-varoitusta
        _ = _currentState;
    }

    private void AimAndShoot(CCSPlayerPawn botPawn, Vector from, Vector to)
    {
        // Nostetaan tähtäystä päätä/rintaa kohti
        Vector headTarget = new Vector(to.X, to.Y, to.Z + 64.0f);

        // Laske kulmat
        QAngle targetAngle = CalculateAngle(from, headTarget);

        // Rekyylin kompensointi (lasketaan Pitch eli X-akselia)
        if (_shotsFired > 2)
        {
            targetAngle.X += _shotsFired * 0.8f; 
        }

        // Asetetaan katsekulmat suoraan oliolle
        if (botPawn.EyeAngles != null)
        {
            botPawn.EyeAngles.X = targetAngle.X;
            botPawn.EyeAngles.Y = targetAngle.Y;
            botPawn.EyeAngles.Z = targetAngle.Z;
        }

        // Reagointiviive ja ampuminen MovementServices-komponentin kautta
        if ((DateTime.Now - _lastTargetSeen).TotalMilliseconds > 150)
        {
            if (botPawn.MovementServices != null)
            {
                botPawn.MovementServices.Buttons.Value |= (ulong)PlayerButtons.Attack;
            }
            _shotsFired++;
        }
    }

    private CCSPlayerController? FindNearestEnemy()
    {
        return Utilities.GetPlayers().FirstOrDefault(p =>
            p.PawnIsAlive &&
            p.TeamNum != _bot.TeamNum &&
            !p.IsBot);
    }

    private QAngle CalculateAngle(Vector from, Vector to)
    {
        float deltaX = to.X - from.X;
        float deltaY = to.Y - from.Y;
        float deltaZ = to.Z - from.Z;

        float distance = (float)Math.Sqrt(deltaX * deltaX + deltaY * deltaY);
        float pitch = (float)(-Math.Atan2(deltaZ, distance) * (180.0 / Math.PI));
        float yaw = (float)(Math.Atan2(deltaY, deltaX) * (180.0 / Math.PI));

        return new QAngle(pitch, yaw, 0);
    }
}