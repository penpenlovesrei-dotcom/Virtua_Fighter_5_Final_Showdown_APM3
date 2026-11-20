using Apm.System.UnityUtil;
using UnityEngine;
using UnityEngine.Events;

namespace Apm.System.GameSelect;

public class MovieButton : MonoBehaviour
{
	private Animator controller;

	private TouchManager.TouchEvents events;

	[SerializeField]
	private UnityEvent onMovieButtonTap = new UnityEvent();

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
		if (onMovieButtonTap != null)
		{
			onMovieButtonTap.Invoke();
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
		controller = GetComponent<Animator>();
		events = new TouchManager.TouchEvents
		{
			Canvas = GetComponent<RectTransform>(),
			Name = "MovieButton",
			TouchDown = null,
			TouchUp = null,
			Move = null,
			MoveEnd = null,
			Tap = OnTap
		};
	}
}
