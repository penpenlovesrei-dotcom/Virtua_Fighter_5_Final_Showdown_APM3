using Apm.System.Setting.Volatile;
using UnityEngine;

namespace Apm.System.GameSelect;

public class IconCanvas : MonoBehaviour
{
	public delegate void IsEnd();

	public class IconInfo
	{
		public Icon Icon { get; set; }

		public float Size { get; set; }

		public float MaxRatio { get; set; }

		public float MaxShadowZ { get; set; }

		public float MinShadowZ { get; set; }
	}

	[SerializeField]
	private GameObject moviePlayer;

	[SerializeField]
	private GameObject newIcon;

	private RectTransform rect;

	private IconInfo info;

	public string Version { get; set; }

	public EMoneyInfo EMoney { get; set; }

	public UiInfo Ui { get; set; }

	public GamePadInfo GamePad { get; set; }

	public MoviePlayer.MovieEnd OnMovieEnd { get; set; }

	public IconCanvasAnimation AnimationController => GetComponent<IconCanvasAnimation>();

	public NewIconAnimation NewIconAnimationController => newIcon.GetComponent<NewIconAnimation>();

	public IconInfo Info
	{
		get
		{
			return info;
		}
		set
		{
			if (info == null)
			{
				info = value;
			}
		}
	}

	public Vector2 Position
	{
		get
		{
			return rect.anchoredPosition;
		}
		set
		{
			rect.anchoredPosition = value;
		}
	}

	public int DisplayOrderIndex
	{
		get
		{
			return rect.GetSiblingIndex();
		}
		set
		{
			rect.SetSiblingIndex(value);
		}
	}

	public void PlayMovie(bool isMute)
	{
		moviePlayer.GetComponent<MoviePlayer>().Play(isMute, OnMovieEnd);
	}

	public void StopMovie()
	{
		moviePlayer.GetComponent<MoviePlayer>().Stop();
	}

	private void Awake()
	{
		rect = GetComponent<RectTransform>();
	}

	private void Start()
	{
		if (info != null)
		{
			info.Icon.Size = new Vector2(info.Size, info.Size);
			float num = info.Size * info.MaxRatio;
			rect.sizeDelta = new Vector2(num, num);
			moviePlayer.GetComponent<MoviePlayer>().name = base.name;
		}
	}

	private void Update()
	{
		if (info != null)
		{
			float num = info.Size * info.MaxRatio / 2f;
			float num2 = info.Size * (info.MaxRatio - 1f) / 2f;
			float num3 = ((!(Mathf.Abs(Position.x) >= num)) ? ((1f - info.MaxRatio) / num * Mathf.Abs(Position.x) + info.MaxRatio) : 1f);
			float x = ((Position.x >= 0f) ? ((!(Mathf.Abs(Position.x) >= num)) ? (Position.x / num * num2) : num2) : ((!(Mathf.Abs(Position.x) >= num)) ? (Position.x / num * num2) : (0f - num2)));
			info.Icon.Scale = new Vector2(num3, num3);
			info.Icon.Position = new Vector2(x, 0f);
			Vector3 localPosition = info.Icon.transform.Find("IconShadow").transform.localPosition;
			float num4 = ((!(Mathf.Abs(Position.x) >= num)) ? ((Info.MaxShadowZ - Info.MinShadowZ) / num * Mathf.Abs(Position.x) - (Info.MaxShadowZ - Info.MinShadowZ)) : 0f);
			info.Icon.transform.Find("IconShadow").transform.localPosition = new Vector3(localPosition.x, localPosition.y, Info.MinShadowZ - num4);
			rect.anchoredPosition3D = new Vector3(rect.anchoredPosition.x, (num3 - 1f) * info.Size / 2f, 0f - num4);
		}
	}
}
