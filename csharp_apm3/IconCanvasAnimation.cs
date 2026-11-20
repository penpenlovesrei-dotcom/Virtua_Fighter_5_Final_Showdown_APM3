using Apm.System.UnityUtil;

namespace Apm.System.GameSelect;

public class IconCanvasAnimation : AnimationController
{
	public enum AnimationType
	{
		ZoomIn,
		MoveLeft,
		MoveRight,
		ZoomOut,
		ReturnLeft,
		ReturnRight,
		ZoomInForMovie,
		ZoomOutForMovie
	}

	public bool IsIdle => IsState("Idle") && !base.IsAnimating;

	public bool IsEnableMovieWindow => IsState("ZoomInForMovieEnd");

	public void StartAnimation(AnimationType type, AnimationEnd onEnd = null, InvalidCondition onInvalidCondition = null)
	{
		string trigger = type.ToString();
		string conditionState = string.Empty;
		string nextState = string.Empty;
		switch (type)
		{
		case AnimationType.ZoomIn:
			conditionState = "Idle";
			nextState = "ZoomInEnd";
			break;
		case AnimationType.MoveLeft:
			conditionState = "Idle";
			nextState = "MoveLeftEnd";
			break;
		case AnimationType.MoveRight:
			conditionState = "Idle";
			nextState = "MoveRightEnd";
			break;
		case AnimationType.ZoomOut:
			conditionState = "ZoomInEnd";
			nextState = "Idle";
			break;
		case AnimationType.ReturnLeft:
			conditionState = "MoveLeftEnd";
			nextState = "Idle";
			break;
		case AnimationType.ReturnRight:
			conditionState = "MoveRightEnd";
			nextState = "Idle";
			break;
		case AnimationType.ZoomInForMovie:
			conditionState = "Idle";
			nextState = "ZoomInForMovieEnd";
			break;
		case AnimationType.ZoomOutForMovie:
			conditionState = "ZoomInForMovieEnd";
			nextState = "Idle";
			break;
		}
		StartCoroutine(StartAnimationCoroutine(conditionState, nextState, trigger, onEnd, onInvalidCondition));
	}
}
