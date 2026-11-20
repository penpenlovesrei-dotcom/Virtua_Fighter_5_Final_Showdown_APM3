using System.Collections.Generic;
using Apm.System.UnityUtil;
using UnityEngine;
using UnityEngine.UI;

namespace Apm.System.GameSelect;

public class TitleAnimation : MonoBehaviour
{
	private enum TitleAnimationState
	{
		Start,
		WaitStart,
		Move,
		End,
		WaitEnd,
		MoveReturn
	}

	[SerializeField]
	private float stopTime = 1f;

	[SerializeField]
	private float titleSpeed = 1f;

	[SerializeField]
	private float titleReturnSpeed = 4f;

	private Vector3 defaultTitlePos;

	private Vector3 titleOffset;

	private TitleAnimationState state;

	private float start;

	[SerializeField]
	private GameObject title;

	[SerializeField]
	private float fadeTime = 0.1f;

	private List<FadeObject> fadeObject;

	private bool isShow;

	public string Title
	{
		get
		{
			return title.GetComponent<Text>().text;
		}
		set
		{
			if (title.GetComponent<Text>().text != value)
			{
				title.GetComponent<Text>().text = value;
				titleOffset = new Vector3((!(title.GetComponent<RectTransform>().sizeDelta.x < title.GetComponent<Text>().preferredWidth)) ? 0f : ((title.GetComponent<Text>().preferredWidth - title.GetComponent<RectTransform>().sizeDelta.x) / 2f), 0f, 0f);
				title.GetComponent<RectTransform>().localPosition = defaultTitlePos + titleOffset;
			}
		}
	}

	public void Hide()
	{
		if (!isShow)
		{
			return;
		}
		isShow = false;
		foreach (FadeObject item in fadeObject)
		{
			StartCoroutine(item.StartFade(fadeIn: false, fadeTime));
		}
	}

	public void Show()
	{
		if (isShow)
		{
			return;
		}
		isShow = true;
		state = TitleAnimationState.Start;
		title.GetComponent<RectTransform>().localPosition = defaultTitlePos + titleOffset;
		foreach (FadeObject item in fadeObject)
		{
			StartCoroutine(item.StartFade(fadeIn: true, fadeTime));
		}
	}

	private void Start()
	{
		fadeObject = FadeObject.EnumFadeObject(base.transform, string.Empty);
		defaultTitlePos = title.GetComponent<RectTransform>().localPosition;
	}

	private void Update()
	{
		if (!(title.GetComponent<RectTransform>().sizeDelta.x < title.GetComponent<Text>().preferredWidth))
		{
			return;
		}
		switch (state)
		{
		case TitleAnimationState.Start:
			start = Time.time;
			state = TitleAnimationState.WaitStart;
			break;
		case TitleAnimationState.WaitStart:
			if (Time.time - start > stopTime)
			{
				state = TitleAnimationState.Move;
			}
			break;
		case TitleAnimationState.Move:
			title.GetComponent<RectTransform>().localPosition += new Vector3(0f - titleSpeed, 0f);
			if (title.GetComponent<RectTransform>().localPosition.x < defaultTitlePos.x - titleOffset.x)
			{
				title.GetComponent<RectTransform>().localPosition = defaultTitlePos - titleOffset;
				state = TitleAnimationState.End;
			}
			break;
		case TitleAnimationState.End:
			start = Time.time;
			state = TitleAnimationState.WaitEnd;
			break;
		case TitleAnimationState.WaitEnd:
			if (Time.time - start > stopTime)
			{
				state = TitleAnimationState.MoveReturn;
			}
			break;
		case TitleAnimationState.MoveReturn:
			title.GetComponent<RectTransform>().localPosition += new Vector3(titleSpeed * titleReturnSpeed, 0f);
			if (title.GetComponent<RectTransform>().localPosition.x > defaultTitlePos.x + titleOffset.x)
			{
				title.GetComponent<RectTransform>().localPosition = defaultTitlePos + titleOffset;
				state = TitleAnimationState.Start;
			}
			break;
		}
	}
}
