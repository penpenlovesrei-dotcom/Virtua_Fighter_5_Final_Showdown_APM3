using System.Collections.Generic;
using Apm.System.UnityUtil;

namespace Apm.System.GameSelect;

public class MainCanvasAnimation : AnimationController
{
	public enum AnimationType
	{
		HideAllPanel,
		ShowAllPanel,
		HideInfoAndGuidePanel,
		ShowInfoAndGuidePanel
	}

	public void StartAnimation(AnimationType type, bool showMessage = false, InvalidCondition onInvalidCondition = null)
	{
		List<string> list = new List<string>();
		string nextState = string.Empty;
		string trigger = string.Empty;
		switch (type)
		{
		case AnimationType.HideAllPanel:
			list.Add("Idle");
			nextState = "HideEnd";
			trigger = "Hide";
			break;
		case AnimationType.ShowAllPanel:
			list.Add("HideEnd");
			nextState = "Idle";
			trigger = "Show";
			break;
		case AnimationType.HideInfoAndGuidePanel:
			list.Add("Idle");
			nextState = "PlayingMovie";
			trigger = "ShowMovie";
			SetValue<bool>("ShowMessage", showMessage);
			break;
		case AnimationType.ShowInfoAndGuidePanel:
			list.Add("PlayingMovie");
			list.Add("PlayingMovieWithMessage");
			nextState = "Idle";
			trigger = "EndMovie";
			break;
		}
		StartCoroutine(StartAnimationCoroutine(list.ToArray(), nextState, trigger, null, onInvalidCondition));
	}
}
