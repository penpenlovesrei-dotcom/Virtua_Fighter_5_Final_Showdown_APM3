using UnityEngine;

namespace Apm.System.GameSelect;

public class Design : MonoBehaviour
{
	[SerializeField]
	private Material backPanel;

	[SerializeField]
	private Material hedderPanel;

	[SerializeField]
	private Material messagePanel;

	[SerializeField]
	private Material bottomPanel;

	[SerializeField]
	private Material movieButton;

	[SerializeField]
	private float panelThickness;

	public Material BackPanel
	{
		get
		{
			return backPanel;
		}
		set
		{
			backPanel = value;
		}
	}

	public Material HedderPanel
	{
		get
		{
			return hedderPanel;
		}
		set
		{
			hedderPanel = value;
		}
	}

	public Material MessagePanel
	{
		get
		{
			return messagePanel;
		}
		set
		{
			messagePanel = value;
		}
	}

	public Material BottomPanel
	{
		get
		{
			return bottomPanel;
		}
		set
		{
			bottomPanel = value;
		}
	}

	public Material MovieButton
	{
		get
		{
			return movieButton;
		}
		set
		{
			movieButton = value;
		}
	}

	public float PanelThickness
	{
		get
		{
			return panelThickness;
		}
		set
		{
			panelThickness = value;
		}
	}
}
