using UnityEngine;
using UnityEngine.UI;

namespace Apm.System.GameSelect;

public class Credit : MonoBehaviour
{
	[SerializeField]
	private string credit = string.Empty;

	[SerializeField]
	private string freePlay = string.Empty;

	private Text value;

	public void OnCreditChange(bool isFreePlay, string creditString)
	{
		if (isFreePlay)
		{
			value.text = freePlay;
		}
		else
		{
			value.text = credit + " " + creditString;
		}
	}

	private void Awake()
	{
		value = base.transform.Find("Value").GetComponent<Text>();
	}
}
