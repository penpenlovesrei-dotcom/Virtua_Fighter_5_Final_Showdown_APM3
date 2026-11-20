using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

namespace Picker;

[AddComponentMenu("UI/Picker/WheelEffect3D", 900)]
public class WheelEffect3D : EffectBase
{
	[SerializeField]
	protected RectTransform.Axis m_Layout = RectTransform.Axis.Vertical;

	[SerializeField]
	protected float m_PolygonSplitLength = 10f;

	[SerializeField]
	protected float m_Radius = 50f;

	public RectTransform.Axis layout
	{
		get
		{
			return m_Layout;
		}
		set
		{
			SetProperty(ref m_Layout, value);
		}
	}

	public float polygonSplitLength
	{
		get
		{
			return m_PolygonSplitLength;
		}
		set
		{
			SetProperty(ref m_PolygonSplitLength, value);
		}
	}

	public float radius
	{
		get
		{
			return m_Radius;
		}
		set
		{
			SetProperty(ref m_Radius, value);
		}
	}

	private static bool Intersect(float d0, float d1, float planeD, out float rate)
	{
		d0 -= planeD;
		d1 -= planeD;
		if (d0 * d1 >= 0f || d0 == d1)
		{
			rate = -1f;
			return false;
		}
		rate = Mathf.Clamp01(d0 / (d0 - d1));
		return true;
	}

	public override void ModifyMesh(VertexHelper vh)
	{
		SplitAndCurveMesh(vh);
	}

	private void SplitAndCurveMesh(VertexHelper vh)
	{
		if (m_PolygonSplitLength <= 0f || !IsActive())
		{
			return;
		}
		Vector3 up = Vector3.up;
		up = ((m_Layout != RectTransform.Axis.Horizontal) ? Vector3.up : Vector3.right);
		List<UIVertex> list = ListPool<UIVertex>.Get();
		vh.GetUIVertexStream(list);
		List<UIVertex> list2 = ListPool<UIVertex>.Get();
		list2.Clear();
		List<UIVertex> list3 = ListPool<UIVertex>.Get();
		list3.Clear();
		List<float> list4 = ListPool<float>.Get();
		list4.Clear();
		try
		{
			float num = float.MinValue;
			float num2 = float.MaxValue;
			int i = 0;
			for (int count = list.Count; i < count; i++)
			{
				float a = Vector3.Dot(list[i].position, up);
				num = Mathf.Max(a, num);
				num2 = Mathf.Min(a, num2);
			}
			float num3 = m_PolygonSplitLength;
			int j = 0;
			for (int count2 = list.Count; j < count2; j += 3)
			{
				UIVertex uIVertex = list[j];
				UIVertex uIVertex2 = list[j + 1];
				UIVertex uIVertex3 = list[j + 2];
				float num4 = 0f - Vector3.Dot(uIVertex.position, up);
				float num5 = 0f - Vector3.Dot(uIVertex2.position, up);
				float num6 = 0f - Vector3.Dot(uIVertex3.position, up);
				list4.Clear();
				list4.Add(0f);
				list4.Add(1f);
				list4.Add(2f);
				for (float num7 = num2 + num3; num7 < num; num7 += num3)
				{
					if (Intersect(num4, num5, num7, out var rate) && rate % 1f != 0f)
					{
						list4.Add(rate);
					}
					if (Intersect(num5, num6, num7, out rate) && rate % 1f != 0f)
					{
						list4.Add(rate + 1f);
					}
					if (Intersect(num6, num4, num7, out rate) && rate % 1f != 0f)
					{
						list4.Add(rate + 2f);
					}
				}
				if (list4.Count == 3)
				{
					list2.Add(uIVertex);
					list2.Add(uIVertex2);
					list2.Add(uIVertex3);
					continue;
				}
				list4.Sort();
				int count3 = list4.Count;
				list3.Clear();
				int num8 = 0;
				float num9 = float.MaxValue;
				for (int k = 0; k < count3; k++)
				{
					float num10 = list4[k];
					int num11 = Mathf.FloorToInt(num10);
					UIVertex uIVertex4 = default(UIVertex);
					uIVertex4 = num11 switch
					{
						0 => EffectBase.Leap(uIVertex, uIVertex2, num10), 
						1 => EffectBase.Leap(uIVertex2, uIVertex3, num10 - 1f), 
						_ => EffectBase.Leap(uIVertex3, uIVertex, num10 - 2f), 
					};
					float num12 = (list4[k] = Vector3.Dot(up, uIVertex4.position));
					list3.Add(uIVertex4);
					if (num9 > num12)
					{
						num8 = k;
						num9 = num12;
					}
				}
				int num14 = (num8 + 1) % count3;
				int num15 = (num8 - 1 + count3) % count3;
				while (num8 != num15 && num8 != num14)
				{
					list2.Add(list3[num8]);
					list2.Add(list3[num14]);
					list2.Add(list3[num15]);
					float num16 = list4[num8];
					if (Mathf.Abs(list4[num14] - num16) > Mathf.Abs(list4[num15] - num16) * 1.0001f)
					{
						num8 = num15;
						num15 = (num8 - 1 + count3) % count3;
					}
					else
					{
						num8 = num14;
						num14 = (num8 + 1) % count3;
					}
				}
			}
			float num17 = (num + num2) * 0.5f;
			float num18 = m_Radius;
			float num19 = 1f / num18;
			int index = ((m_Layout == RectTransform.Axis.Vertical) ? 1 : 0);
			int l = 0;
			for (int count4 = list2.Count; l < count4; l++)
			{
				UIVertex value = list2[l];
				Vector3 position = value.position;
				float num20 = Vector3.Dot(position, up);
				float f = (num20 - num17) * num19;
				position[index] = Mathf.Sin(f) * num18;
				position.z = num18 - Mathf.Cos(f) * num18;
				value.position = position;
				list2[l] = value;
			}
			vh.Clear();
			vh.AddUIVertexTriangleStream(list2);
		}
		finally
		{
			ListPool<UIVertex>.Release(list);
			ListPool<UIVertex>.Release(list2);
			ListPool<UIVertex>.Release(list3);
			ListPool<float>.Release(list4);
		}
	}
}
