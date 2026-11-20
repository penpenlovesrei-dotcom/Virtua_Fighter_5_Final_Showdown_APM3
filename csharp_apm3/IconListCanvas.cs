using System;
using System.Collections.Generic;
using System.Linq;
using Apm.System.Setting.Volatile;
using Apm.System.UnityUtil;
using UnityEngine;
using UnityEngine.Events;

namespace Apm.System.GameSelect;

public class IconListCanvas : MonoBehaviour
{
	public enum AnimationType
	{
		StartGame,
		CancelStartGame,
		ShowMovie,
		EndMovie
	}

	[Serializable]
	private class SelectIconEvent : UnityEvent<string, string, AppAdditionalInfo>
	{
	}

	[Serializable]
	private class SelectableChangeEvent : UnityEvent<bool>
	{
	}

	[SerializeField]
	private GameObject iconPrefab;

	[SerializeField]
	private GameObject title;

	[SerializeField]
	private GameObject backGround;

	[SerializeField]
	private GameObject leftButton;

	[SerializeField]
	private GameObject rightButton;

	[SerializeField]
	private GameObject changeSoundPlayArea;

	[SerializeField]
	private Vector2 accel = new Vector2(-1f, 0f);

	[SerializeField]
	private float rangeOfMovement = 0.5f;

	private Dictionary<string, IconCanvas> icons = new Dictionary<string, IconCanvas>();

	private Vector2 speed;

	private bool isInertiaMove;

	private bool isMoving;

	[SerializeField]
	private float iconSize = 256f;

	[SerializeField]
	private float gapSize = 16f;

	[SerializeField]
	private float selectedIconRatio = 1.5f;

	[SerializeField]
	private float selectedIconShadowZ = -24f;

	[SerializeField]
	private float iconShadowZ = -16f;

	private List<IconCanvas> iconsOrder = new List<IconCanvas>();

	private int index;

	private Vector2 conditionSpeed;

	[SerializeField]
	private UnityEvent onIconThroughSelectedArea = new UnityEvent();

	[SerializeField]
	private UnityEvent onMovieTap = new UnityEvent();

	[SerializeField]
	private SelectIconEvent onSelectIcon = new SelectIconEvent();

	[SerializeField]
	private UnityEvent onMovieEnd = new UnityEvent();

	[SerializeField]
	private SelectableChangeEvent onSelectableChange = new SelectableChangeEvent();

	public bool IsBusy => IsAnimating || IsMoving;

	public bool IsPlayingMovie { get; set; }

	public bool IsEnableMovieWindow => !IsAnimating && iconsOrder[index].AnimationController.IsEnableMovieWindow;

	public string Version => iconsOrder[index].Version;

	public EMoneyInfo EMoney => iconsOrder[index].EMoney;

	public UiInfo Ui => iconsOrder[index].Ui;

	public GamePadInfo GamePad => iconsOrder[index].GamePad;

	public bool IsMoving
	{
		get
		{
			return isMoving;
		}
		private set
		{
			if (isMoving != value)
			{
				if (onSelectableChange != null)
				{
					onSelectableChange.Invoke(!value);
				}
				isMoving = value;
			}
		}
	}

	public bool CanSelect => IsIdle && !IsMoving;

	public UnityEvent OnIconThroughSelectedArea
	{
		get
		{
			return onIconThroughSelectedArea;
		}
		set
		{
			onIconThroughSelectedArea = value;
		}
	}

	private bool CanMove => IsIdle;

	private bool IsAnimating
	{
		get
		{
			bool result = false;
			foreach (IconCanvas item in iconsOrder)
			{
				if (item.AnimationController.IsAnimating)
				{
					result = true;
					break;
				}
			}
			return result;
		}
	}

	private bool IsEnableLeftButton => index - 3 >= 0;

	private bool IsEnableRightButton => index + 3 < iconsOrder.Count;

	private bool IsIdle
	{
		get
		{
			foreach (IconCanvas item in iconsOrder)
			{
				if (!item.AnimationController.IsIdle)
				{
					return false;
				}
			}
			return true;
		}
	}

	public void OnTouchDown(string name, Vector2 pos)
	{
		if (CanMove)
		{
			speed = Vector2.zero;
		}
	}

	public void OnMove(string name, Vector2 delta)
	{
		if (!CanMove)
		{
			return;
		}
		IsMoving = true;
		if (iconsOrder[0].GetComponent<RectTransform>().anchoredPosition.x + delta.x >= iconSize * rangeOfMovement)
		{
			delta = new Vector2(iconSize * rangeOfMovement - iconsOrder[0].GetComponent<RectTransform>().anchoredPosition.x, delta.y);
		}
		else if (iconsOrder[iconsOrder.Count - 1].GetComponent<RectTransform>().anchoredPosition.x + delta.x <= 0f - iconSize * rangeOfMovement)
		{
			delta = new Vector2(0f - iconSize * rangeOfMovement - iconsOrder[iconsOrder.Count - 1].GetComponent<RectTransform>().anchoredPosition.x, delta.y);
		}
		foreach (KeyValuePair<string, IconCanvas> icon in icons)
		{
			icon.Value.GetComponent<RectTransform>().anchoredPosition += new Vector2(delta.x, 0f);
		}
	}

	public void OnMoveEnd(string name, Vector2 speed)
	{
		if (CanMove)
		{
			if (Mathf.Abs(speed.x) < Mathf.Abs(conditionSpeed.x) / 4f)
			{
				Select(GetNearCenterIcon());
				return;
			}
			isInertiaMove = true;
			this.speed = speed;
		}
	}

	public void OnTap(string name, Vector2 pos)
	{
		if (IsEnableMovieWindow)
		{
			if (onMovieTap != null)
			{
				onMovieTap.Invoke();
			}
		}
		else
		{
			if (!CanMove)
			{
				return;
			}
			if (IsMoving)
			{
				Select(GetNearCenterIcon());
			}
			else
			{
				if (!icons.ContainsKey(name))
				{
					return;
				}
				if (name == iconsOrder[index].name)
				{
					AppAdditionalInfo appAdditionalInfo = new AppAdditionalInfo();
					appAdditionalInfo.EMoney = iconsOrder[index].EMoney;
					appAdditionalInfo.Ui = iconsOrder[index].Ui;
					appAdditionalInfo.GamePad = iconsOrder[index].GamePad;
					AppAdditionalInfo arg = appAdditionalInfo;
					if (onSelectIcon != null)
					{
						onSelectIcon.Invoke(base.name, iconsOrder[index].Version, arg);
					}
				}
				else
				{
					Select(icons[name]);
				}
			}
		}
	}

	public void OnEnter()
	{
		if (CanMove && IsMoving)
		{
			OnIconThroughSelectedArea?.Invoke();
		}
	}

	public void MoveLeft()
	{
		if (CanMove)
		{
			speed = -(conditionSpeed - accel);
			isInertiaMove = true;
			index = iconsOrder.FindIndex((IconCanvas a) => a == GetNextSelectIcon());
			base.name = iconsOrder[index].name;
			IsMoving = true;
		}
	}

	public void MoveRight()
	{
		if (CanMove)
		{
			speed = conditionSpeed - accel;
			isInertiaMove = true;
			index = iconsOrder.FindIndex((IconCanvas a) => a == GetNextSelectIcon());
			base.name = iconsOrder[index].name;
			IsMoving = true;
		}
	}

	public void MoveNext()
	{
		if (CanSelect)
		{
			int num = ((index + 1 < iconsOrder.Count) ? (index + 1) : 0);
			Select(iconsOrder[num]);
		}
	}

	public void StartAnimation(AnimationType type, AnimationController.AnimationEnd onEnd = null, AnimationController.InvalidCondition onInvalidCondition = null)
	{
		IconCanvasAnimation.AnimationType type2;
		IconCanvasAnimation.AnimationType type3;
		IconCanvasAnimation.AnimationType type4;
		switch (type)
		{
		case AnimationType.StartGame:
			type2 = IconCanvasAnimation.AnimationType.ZoomIn;
			type3 = IconCanvasAnimation.AnimationType.MoveLeft;
			type4 = IconCanvasAnimation.AnimationType.MoveRight;
			break;
		case AnimationType.CancelStartGame:
			type2 = IconCanvasAnimation.AnimationType.ZoomOut;
			type3 = IconCanvasAnimation.AnimationType.ReturnLeft;
			type4 = IconCanvasAnimation.AnimationType.ReturnRight;
			break;
		case AnimationType.ShowMovie:
			type2 = IconCanvasAnimation.AnimationType.ZoomInForMovie;
			type3 = IconCanvasAnimation.AnimationType.MoveLeft;
			type4 = IconCanvasAnimation.AnimationType.MoveRight;
			break;
		case AnimationType.EndMovie:
			type2 = IconCanvasAnimation.AnimationType.ZoomOutForMovie;
			type3 = IconCanvasAnimation.AnimationType.ReturnLeft;
			type4 = IconCanvasAnimation.AnimationType.ReturnRight;
			break;
		default:
			type2 = IconCanvasAnimation.AnimationType.ZoomIn;
			type3 = IconCanvasAnimation.AnimationType.MoveLeft;
			type4 = IconCanvasAnimation.AnimationType.MoveRight;
			break;
		}
		for (int i = 0; i < iconsOrder.Count; i++)
		{
			if (index == i)
			{
				iconsOrder[i].AnimationController.StartAnimation(type2, onEnd, onInvalidCondition);
				iconsOrder[i].NewIconAnimationController.Hide();
			}
			else if (index < i)
			{
				iconsOrder[i].AnimationController.StartAnimation(type4, null, onInvalidCondition);
			}
			else
			{
				iconsOrder[i].AnimationController.StartAnimation(type3, null, onInvalidCondition);
			}
		}
	}

	public void ShowNewIcon()
	{
		iconsOrder[index].NewIconAnimationController.Show();
	}

	public void StartMovie(bool isMute)
	{
		if (!IsPlayingMovie)
		{
			iconsOrder[index].PlayMovie(isMute);
			IsPlayingMovie = true;
		}
	}

	public void StopMovie()
	{
		if (IsPlayingMovie)
		{
			iconsOrder[index].StopMovie();
			IsPlayingMovie = false;
		}
	}

	public void OnPageButtonTap(bool isLeft)
	{
		int num = index;
		if (isLeft)
		{
			num -= 5;
			num = ((num >= 0) ? num : 0);
		}
		else
		{
			num += 5;
			num = ((num < iconsOrder.Count) ? num : (iconsOrder.Count - 1));
		}
		Select(iconsOrder[num]);
	}

	private void Awake()
	{
		speed = Vector2.zero;
		isInertiaMove = false;
		conditionSpeed = Vector2.zero;
		index = 0;
		IsMoving = false;
	}

	private void Start()
	{
		int num = 0;
		List<AppInfo> list = (from info in AppListManager.GetInstance().Info.SelectableList
			where info.New
			orderby info.StartDate descending
			select info).ToList();
		list.AddRange((from info in AppListManager.GetInstance().Info.SelectableList
			where !info.New
			orderby info.StartDate descending
			select info).ToList());
		foreach (AppInfo item in list)
		{
			GameObject gameObject = UnityEngine.Object.Instantiate(iconPrefab, base.transform);
			IconCanvas component = gameObject.GetComponent<IconCanvas>();
			component.name = item.SubGameId;
			component.Version = item.Version;
			component.EMoney = item.EMoney;
			component.Ui = item.Ui;
			component.GamePad = item.GamePad;
			Icon component2 = component.transform.Find("AnimationCanvas").transform.Find("Icon").GetComponent<Icon>();
			component2.name = item.SubGameId;
			component.Position = new Vector2((float)num * (iconSize + gapSize), 0f);
			component2.Path = item.Paths.Icon;
			component2.TitleName = item.TitleName;
			component2.IsNew = item.New;
			component2.TouchEvents = new TouchManager.TouchEvents
			{
				Canvas = GetComponent<RectTransform>(),
				Name = item.SubGameId,
				TouchDown = OnTouchDown,
				TouchUp = null,
				Move = OnMove,
				MoveEnd = OnMoveEnd,
				Tap = OnTap
			};
			component.Info = new IconCanvas.IconInfo
			{
				Icon = component2,
				Size = iconSize,
				MaxRatio = selectedIconRatio,
				MaxShadowZ = selectedIconShadowZ,
				MinShadowZ = iconShadowZ
			};
			component.OnMovieEnd = OnMovieEnd;
			BoxCollider2D component3 = component2.GetComponent<BoxCollider2D>();
			component3.size = new Vector2(iconSize, iconSize);
			icons.Add(component2.name, component);
			iconsOrder.Add(component);
			if (item.SubGameId == SequenceSettingManager.GetInstance().Info.SubGameId)
			{
				index = num;
			}
			num++;
		}
		BoxCollider2D component4 = changeSoundPlayArea.GetComponent<BoxCollider2D>();
		component4.size = new Vector2(iconSize, iconSize);
		float num2 = Mathf.Abs(accel.x);
		float num3 = 0f;
		while (num3 < iconSize)
		{
			num3 += num2;
			num2 += Mathf.Abs(accel.x);
		}
		conditionSpeed = new Vector2(num2, 0f);
		base.name = iconsOrder[index].name;
		title.GetComponent<TitleAnimation>().Title = iconsOrder[index].GetComponent<IconCanvas>().Info.Icon.TitleName;
		AlignmentIcon(index);
		backGround.GetComponent<IconListBackground>().TouchEvents = new TouchManager.TouchEvents
		{
			Canvas = GetComponent<RectTransform>(),
			Name = "Background",
			TouchDown = OnTouchDown,
			TouchUp = null,
			Move = OnMove,
			MoveEnd = OnMoveEnd,
			Tap = OnTap
		};
	}

	private void Update()
	{
		leftButton.GetComponent<PageButton>().Show = !IsMoving && IsEnableLeftButton;
		rightButton.GetComponent<PageButton>().Show = !IsMoving && IsEnableRightButton;
		if (!IsAnimating)
		{
			if (speed != Vector2.zero)
			{
				IntertialMove();
			}
			Sort();
		}
		if (CanSelect)
		{
			title.GetComponent<TitleAnimation>().Title = iconsOrder[index].GetComponent<IconCanvas>().Info.Icon.TitleName;
			title.GetComponent<TitleAnimation>().Show();
		}
		else
		{
			title.GetComponent<TitleAnimation>().Hide();
		}
	}

	private void Sort()
	{
		List<KeyValuePair<string, IconCanvas>> list = new List<KeyValuePair<string, IconCanvas>>(icons);
		list.Sort((KeyValuePair<string, IconCanvas> a, KeyValuePair<string, IconCanvas> b) => (int)(Mathf.Abs(b.Value.Position.x) - Mathf.Abs(a.Value.Position.x)));
		int num = 0;
		foreach (KeyValuePair<string, IconCanvas> item in list)
		{
			item.Value.DisplayOrderIndex = num;
			num++;
		}
		leftButton.GetComponent<RectTransform>().SetSiblingIndex(num++);
		rightButton.GetComponent<RectTransform>().SetSiblingIndex(num++);
		backGround.GetComponent<RectTransform>().SetAsFirstSibling();
	}

	private void Select(IconCanvas target)
	{
		float num = Mathf.Abs(accel.x);
		float num2 = 0f;
		while (num2 < Mathf.Abs(target.GetComponent<RectTransform>().anchoredPosition.x))
		{
			num2 += num;
			num += Mathf.Abs(accel.x);
		}
		speed = new Vector2((!(target.GetComponent<RectTransform>().anchoredPosition.x > 0f)) ? num : (0f - num), 0f);
		index = iconsOrder.FindIndex((IconCanvas a) => a == target);
		base.name = iconsOrder[index].name;
		IsMoving = true;
	}

	private void IntertialMove()
	{
		foreach (KeyValuePair<string, IconCanvas> icon in icons)
		{
			icon.Value.GetComponent<RectTransform>().anchoredPosition += new Vector2(speed.x, 0f);
		}
		float num = Mathf.Abs(speed.x) - Mathf.Abs(accel.x);
		if (num < 0f)
		{
			speed = Vector2.zero;
		}
		else
		{
			speed = new Vector2((!(speed.x > 0f)) ? (0f - num) : num, 0f);
		}
		if (Mathf.Abs(speed.x) >= Mathf.Abs(conditionSpeed.x))
		{
			if (iconsOrder[0].GetComponent<RectTransform>().anchoredPosition.x >= iconSize * rangeOfMovement)
			{
				AlignmentIcon(0, iconSize * rangeOfMovement);
				Select(iconsOrder[0]);
			}
			else if (iconsOrder[iconsOrder.Count - 1].GetComponent<RectTransform>().anchoredPosition.x <= 0f - iconSize * rangeOfMovement)
			{
				AlignmentIcon(iconsOrder.Count - 1, 0f - iconSize * rangeOfMovement);
				Select(iconsOrder[iconsOrder.Count - 1]);
			}
			return;
		}
		if (isInertiaMove)
		{
			Select(GetNextSelectIcon());
			isInertiaMove = false;
		}
		if ((speed.x > 0f && iconsOrder[index].GetComponent<RectTransform>().anchoredPosition.x > 0f) || (speed.x < 0f && iconsOrder[index].GetComponent<RectTransform>().anchoredPosition.x < 0f) || (speed == Vector2.zero && iconsOrder[index].GetComponent<RectTransform>().anchoredPosition.x != 0f))
		{
			AlignmentIcon(index);
			IsMoving = false;
		}
	}

	private IconCanvas GetNearCenterIcon()
	{
		List<KeyValuePair<string, IconCanvas>> list = new List<KeyValuePair<string, IconCanvas>>(icons);
		list.Sort((KeyValuePair<string, IconCanvas> a, KeyValuePair<string, IconCanvas> b) => (int)(Mathf.Abs(a.Value.Position.x) - Mathf.Abs(b.Value.Position.x)));
		return list[0].Value;
	}

	private IconCanvas GetNextSelectIcon()
	{
		IconCanvas iconCanvas;
		if (speed.x > 0f)
		{
			iconCanvas = iconsOrder[0];
			foreach (KeyValuePair<string, IconCanvas> icon in icons)
			{
				if (iconCanvas.GetComponent<RectTransform>().anchoredPosition.x < icon.Value.GetComponent<RectTransform>().anchoredPosition.x && icon.Value.GetComponent<RectTransform>().anchoredPosition.x <= 0f)
				{
					iconCanvas = icon.Value;
				}
			}
		}
		else
		{
			iconCanvas = iconsOrder[iconsOrder.Count - 1];
			foreach (KeyValuePair<string, IconCanvas> icon2 in icons)
			{
				if (iconCanvas.GetComponent<RectTransform>().anchoredPosition.x > icon2.Value.GetComponent<RectTransform>().anchoredPosition.x && icon2.Value.GetComponent<RectTransform>().anchoredPosition.x >= 0f)
				{
					iconCanvas = icon2.Value;
				}
			}
		}
		return iconCanvas;
	}

	private void AlignmentIcon(int selectedIndex, float offset = 0f)
	{
		float num = gapSize + iconSize;
		for (int i = 0; i < iconsOrder.Count; i++)
		{
			iconsOrder[i].GetComponent<RectTransform>().anchoredPosition = new Vector2((0f - num) * (float)(selectedIndex - i) + offset, 0f);
		}
		speed = Vector2.zero;
	}

	private void OnMovieEnd()
	{
		if (onMovieEnd != null)
		{
			onMovieEnd.Invoke();
		}
	}
}
