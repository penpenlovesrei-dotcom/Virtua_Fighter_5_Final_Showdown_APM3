using Apm.System.UnityUtil;
using UnityEngine;
using UnityEngine.UI;

namespace Apm.System.GameSelect;

public class Icon : MonoBehaviour
{
	private RectTransform rect;

	private Image image;

	private Renderer shadowRenderer;

	private TouchManager.TouchEvents touchEvents;

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

	public Vector2 Size
	{
		get
		{
			return rect.sizeDelta;
		}
		set
		{
			rect.sizeDelta = value;
		}
	}

	public Vector2 Scale
	{
		get
		{
			return rect.localScale;
		}
		set
		{
			rect.localScale = new Vector3(value.x, value.y, rect.localScale.z);
		}
	}

	public Color Color
	{
		get
		{
			return image.color;
		}
		set
		{
			image.color = value;
		}
	}

	public int SiblingIndex
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

	public TouchManager.TouchEvents TouchEvents
	{
		get
		{
			return touchEvents;
		}
		set
		{
			touchEvents = value;
		}
	}

	public string Path { get; set; }

	public string TitleName { get; set; }

	public bool IsNew
	{
		get
		{
			return base.transform.Find("New").gameObject.activeInHierarchy;
		}
		set
		{
			base.transform.Find("New").gameObject.SetActive(value);
			base.transform.Find("New").gameObject.GetComponent<NewIconAnimation>().Show();
		}
	}

	public void TouchDown()
	{
		GameObject.Find("TouchManager").GetComponent<TouchManager>().OnTouchDown(TouchEvents, Input.mousePosition);
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
		rect = GetComponent<RectTransform>();
		image = base.transform.Find("Texture").GetComponent<Image>();
		shadowRenderer = base.transform.Find("IconShadow").GetComponent<Renderer>();
	}

	private void Start()
	{
		if (Path != null)
		{
			DynamicPngTexture dynamicPngTexture = new DynamicPngTexture();
			Texture2D texture2D = dynamicPngTexture.ReadFileAsTexture(Path);
			if (texture2D != null)
			{
				image.sprite = Sprite.Create(texture2D, new Rect(0f, 0f, texture2D.width, texture2D.height), Vector2.zero);
				shadowRenderer.material.SetTexture("_MainTex", texture2D);
			}
		}
	}
}
