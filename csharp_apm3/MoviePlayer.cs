using Apm.System.Setting.Volatile;
using RenderHeads.Media.AVProVideo;
using UnityEngine;

namespace Apm.System.GameSelect;

public class MoviePlayer : MonoBehaviour
{
	public delegate void MovieEnd();

	[SerializeField]
	private MediaPlayer mediaPlayer;

	private MovieEnd onMovieEnd;

	public void Play(bool isMute, MovieEnd end = null)
	{
		GetComponent<RectTransform>().sizeDelta = new Vector2(1920f, 1080f);
		mediaPlayer.Control.MuteAudio(isMute);
		mediaPlayer.Play();
		onMovieEnd = end;
	}

	public void Stop()
	{
		GetComponent<RectTransform>().sizeDelta = new Vector2(0f, 0f);
		Reload();
	}

	private void Awake()
	{
	}

	private void Start()
	{
		mediaPlayer.OpenVideoFromFile(MediaPlayer.FileLocation.AbsolutePathOrURL, AppListManager.GetInstance().Get(base.name).Paths.Movie, autoPlay: false);
		mediaPlayer.Events.AddListener(MoveEventListener);
	}

	private void MoveEventListener(MediaPlayer player, MediaPlayerEvent.EventType type, ErrorCode err)
	{
		if (type == MediaPlayerEvent.EventType.FinishedPlaying)
		{
			Stop();
			if (onMovieEnd != null)
			{
				onMovieEnd();
			}
		}
	}

	private void Reload()
	{
		mediaPlayer.Stop();
		mediaPlayer.CloseVideo();
		mediaPlayer.OpenVideoFromFile(MediaPlayer.FileLocation.AbsolutePathOrURL, AppListManager.GetInstance().Get(base.name).Paths.Movie, autoPlay: false);
	}
}
