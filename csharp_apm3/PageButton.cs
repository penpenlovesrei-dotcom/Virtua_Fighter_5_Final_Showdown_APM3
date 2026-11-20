using System;
using Apm.System.UnityUtil;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Apm.System.GameSelect;

public class PageButton : MonoBehaviour
{
	[Serializable]
	private class PageEvent : UnityEvent<bool>
	{
	}

	private Animator controller;

	[SerializeField]
	private GameObject button;

	private Image image;

	private TouchManager.TouchEvents events;

	[SerializeField]
	private bool isLeft;

	private float defaultAlpha;

	[SerializeField]
	private PageEvent onPageButtonTap = new PageEvent();

	public bool Show
	{
		get
		{
			return image.color.a != 0f;
		}
		set
		{
			image.color = new Color(image.color.r, image.color.g, image.color.b, (!value) ? 0f : defaultAlpha);
		}
	}

	public void OnSelectableChange(bool selectable)
	{
		if (selectable)
		{
			controller.SetTrigger("Show");
		}
		else
		{
			controller.SetTrigger("Hide");
		}
	}

	public void OnTap(string name, Vector2 pos)
	{
		if (Show && onPageButtonTap != null)
		{
			onPageButtonTap.Invoke(isLeft);
		}
	}

	public void TouchDown()
	{
		GameObject.Find("TouchManager").GetComponent<TouchManager>().OnTouchDown(events, Input.mousePosition);
	}

	public void TouchMove()
	{
		GameObject.Find("TouchManager").GetComponent<TouchManager>().OnTouchMove(Input.mousePosition);
	}

	public void TouchUp()
	{
		GameObject.Find("TouchManager").GetComponent<TouchManager>().OnTouchUp();
	}

	private void Awake()
	{
		image = button.GetComponent<Image>();
		defaultAlpha = image.color.a;
		controller = GetComponent<Animator>();
		events = new TouchManager.TouchEvents
		{
			Canvas = GetComponent<RectTransform>(),
			Name = "Page" + ((!isLeft) ? "Right" : "Left") + "Button",
			TouchDown = null,
			TouchUp = null,
			Move = null,
			MoveEnd = null,
			Tap = OnTap
		};
	}
}
