using System;
using System.Collections;
using AMDaemon;
using Apm.System.AbaasGs;
using Apm.System.Daemon;
using Apm.System.Setting.NonVolatile;
using Apm.System.Setting.Volatile;
using Apm.System.UnityUtil;
using Apm.System.Util;
using Apm.System.Util.Log;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.SceneManagement;

namespace Apm.System.GameSelect;

public class SceneManager : MonoBehaviour
{
	private enum AdvertizeState
	{
		StartMovie,
		WaitMovieStartAnimation,
		WaitMovie,
		WaitMovieEndAnimation,
		WaitCanMove,
		WaitMove
	}

	private enum InputInfo
	{
		None,
		Touch,
		Push01,
		Push02,
		PushOther,
		Credit
	}

	[Serializable]
	private class CreditEvent : UnityEvent<bool, string>
	{
	}

	[Serializable]
	private class StartGameEvent : UnityEvent<string>
	{
	}

	[SerializeField]
	private GameObject daemon;

	private Apm.System.Daemon.Main daemonMain;

	[SerializeField]
	private GameObject generalSetting;

	[SerializeField]
	private GameObject iconListObject;

	[SerializeField]
	private GameObject mainCanvasobject;

	[SerializeField]
	private GameObject headphoneUi;

	[SerializeField]
	private StartGameEvent onGameStart = new StartGameEvent();

	[SerializeField]
	private CreditEvent onChangeCredit = new CreditEvent();

	[SerializeField]
	private UnityEvent onStartAdvertize = new UnityEvent();

	[SerializeField]
	private UnityEvent onEndAdvertize = new UnityEvent();

	private SystemSequenceManager systemSequenceManager;

	[SerializeField]
	private GameObject abaasGsController;

	private bool bootApplication = true;

	[SerializeField]
	private bool isMountEnd;

	[SerializeField]
	private bool isStartGameEnd;

	[SerializeField]
	private bool isStartingGame;

	[SerializeField]
	private bool isCancelPlayMovie;

	private IconListCanvas iconListCanvas;

	private MainCanvasAnimation mainCanvas;

	private float advertizeTime = 20f;

	private string launchSubGameId;

	private string launchVersion;

	[SerializeField]
	private float elapsedTime;

	private InputInfo inputInfo;

	public float RemainTime => advertizeTime - elapsedTime;

	public bool CanSelect => iconListCanvas.CanSelect;

	public string SelectedSubGameId => iconListCanvas.name;

	private bool IsAdvertize => advertizeTime <= elapsedTime;

	[SerializeField]
	private bool IsEnd => isMountEnd && isStartGameEnd && !mainCanvas.IsAnimating && !iconListCanvas.IsBusy;

	public void OnLeftLeverOn()
	{
		iconListCanvas.MoveLeft();
	}

	public void OnRightLeverOn()
	{
		iconListCanvas.MoveRight();
	}

	public void OnPush01OnNow()
	{
		if (iconListCanvas.CanSelect)
		{
			AppAdditionalInfo appAdditionalInfo = new AppAdditionalInfo();
			appAdditionalInfo.EMoney = iconListCanvas.EMoney;
			appAdditionalInfo.Ui = iconListCanvas.Ui;
			appAdditionalInfo.GamePad = iconListCanvas.GamePad;
			AppAdditionalInfo info = appAdditionalInfo;
			GameStart(iconListCanvas.name, iconListCanvas.Version, info);
		}
		else
		{
			inputInfo = InputInfo.Push01;
			CancelPlayMovie();
		}
		ResetElapsedTime();
	}

	public void OnPush02OnNow()
	{
		if (iconListCanvas.CanSelect)
		{
			PlayMovie();
		}
		else
		{
			inputInfo = InputInfo.Push02;
			CancelPlayMovie();
		}
		ResetElapsedTime();
	}

	public void OnPushOtherOnNow()
	{
		inputInfo = InputInfo.PushOther;
		CancelPlayMovie();
		ResetElapsedTime();
	}

	public void OnErrorOccurred(ErrorInfo info)
	{
		abaasGsController.GetComponent<Apm.System.AbaasGs.Main>().Cancel();
		UnityEngine.SceneManagement.SceneManager.LoadScene("Error");
	}

	public void OnMovieEnd()
	{
		inputInfo = InputInfo.None;
		StopMovie();
	}

	public void OnChangeCredit(bool isFreePlay, string creditString)
	{
		if (onChangeCredit != null)
		{
			onChangeCredit.Invoke(isFreePlay, creditString);
		}
		inputInfo = InputInfo.Credit;
		CancelPlayMovie();
		ResetElapsedTime();
	}

	public void GameStart(string subGameId, string version, AppAdditionalInfo info)
	{
		isStartingGame = true;
		launchSubGameId = subGameId;
		launchVersion = version;
		if (!bootApplication)
		{
			isMountEnd = true;
			isStartGameEnd = true;
		}
		else
		{
			SystemConfigManager.GetInstance().Info.EMoney = info.EMoney;
			SystemConfigManager.GetInstance().Info.Ui = info.Ui;
			SystemConfigManager.GetInstance().Info.GamePad = info.GamePad;
			AppMounter.Mount(subGameId, OnMountEnd);
			PlayLogSender.Save("Launch " + subGameId + " Ver." + version);
			abaasGsController.GetComponent<Apm.System.AbaasGs.Main>().Cancel();
			daemonMain.StartGame(subGameId, OnStartGameEnd);
		}
		iconListCanvas.StartAnimation(IconListCanvas.AnimationType.StartGame, null, OnAnimationError);
		mainCanvas.StartAnimation(MainCanvasAnimation.AnimationType.HideAllPanel, showMessage: false, OnAnimationError);
		if (onGameStart != null)
		{
			onGameStart.Invoke(subGameId);
		}
	}

	public void BeginTest()
	{
		if (!isStartingGame)
		{
			daemonMain.BeginTest();
			PlayLogSender.Save("Launch sub system test mode");
			abaasGsController.GetComponent<Apm.System.AbaasGs.Main>().Cancel();
			UnityEngine.SceneManagement.SceneManager.LoadScene("SubSystemTest");
		}
	}

	private void Awake()
	{
		daemonMain = daemon.GetComponent<Apm.System.Daemon.Main>();
		systemSequenceManager = new SystemSequenceManager(daemonMain);
		iconListCanvas = iconListObject.GetComponent<IconListCanvas>();
		mainCanvas = mainCanvasobject.GetComponent<MainCanvasAnimation>();
		isMountEnd = false;
		isStartGameEnd = false;
	}

	private void Start()
	{
		GeneralSetting setting = generalSetting.GetComponent<GeneralSettingAccessor>().Setting;
		bootApplication = !setting.Debug || setting.GameSelectDebugSetting.BootApplication;
		advertizeTime = setting.GameSelectSetting.AdvertizeTime;
		daemonMain.IsEndFirstAccounting = SequenceSettingManager.GetInstance().Info.FirstAccountingReport;
		daemonMain.IsForceReboot = systemSequenceManager.IsRebootNeeded;
	}

	private void Update()
	{
		if (iconListCanvas.CanSelect)
		{
			isCancelPlayMovie = false;
		}
		if (UnityEngine.Input.GetMouseButton(0) && !headphoneUi.GetComponent<HeadphoneMenu>().IsTouchHeadphoneUiArea(UnityEngine.Input.mousePosition))
		{
			ResetElapsedTime();
			if (!iconListCanvas.CanSelect)
			{
				inputInfo = InputInfo.Touch;
				CancelPlayMovie();
			}
		}
		if (CanSelect)
		{
			UpdateElapsedTime();
		}
		if (IsEnd)
		{
			if (!bootApplication)
			{
				iconListCanvas.StartAnimation(IconListCanvas.AnimationType.CancelStartGame, iconListCanvas.ShowNewIcon, OnAnimationError);
				mainCanvas.StartAnimation(MainCanvasAnimation.AnimationType.ShowAllPanel, showMessage: false, OnAnimationError);
				isMountEnd = false;
				isStartGameEnd = false;
				isStartingGame = false;
			}
			else
			{
				systemSequenceManager.Exit(SystemSequenceManager.NextProcess.Game, launchSubGameId, launchVersion);
			}
		}
		if (daemonMain.IsExitNeeded || daemonMain.IsRebootNeeded)
		{
			if (daemonMain.IsRebootNeeded)
			{
				systemSequenceManager.IsRebootNeeded = true;
			}
			UnityEngine.SceneManagement.SceneManager.LoadScene("Setup");
		}
	}

	private void OnStartMovieAnimationEnd()
	{
		if (isCancelPlayMovie)
		{
			StopMovie();
		}
		else
		{
			iconListCanvas.StartMovie(IsAdvertize && !SystemConfigManager.GetInstance().Info.EnableAdvertizeSound);
		}
	}

	private void OnMountEnd(bool isSucceeded)
	{
		if (isSucceeded)
		{
			isMountEnd = true;
		}
		else
		{
			daemonMain.SetError(87);
		}
	}

	private void ResetElapsedTime()
	{
		if (IsAdvertize)
		{
			if (onEndAdvertize != null)
			{
				onEndAdvertize.Invoke();
			}
			StopCoroutine("Advertize");
		}
		elapsedTime = 0f;
	}

	private void UpdateElapsedTime()
	{
		bool isAdvertize = IsAdvertize;
		elapsedTime += Time.deltaTime;
		if (!isAdvertize && IsAdvertize)
		{
			if (onStartAdvertize != null)
			{
				onStartAdvertize.Invoke();
			}
			StartCoroutine("Advertize");
		}
	}

	private void OnStartGameEnd(bool isSucceeded)
	{
		isStartGameEnd = true;
	}

	private IEnumerator Advertize()
	{
		AdvertizeState state = AdvertizeState.StartMovie;
		while (true)
		{
			switch (state)
			{
			case AdvertizeState.StartMovie:
				if (iconListCanvas.CanSelect)
				{
					PlayMovie();
					state = AdvertizeState.WaitMovieStartAnimation;
				}
				break;
			case AdvertizeState.WaitMovieStartAnimation:
				if (iconListCanvas.IsEnableMovieWindow)
				{
					state = AdvertizeState.WaitMovie;
				}
				break;
			case AdvertizeState.WaitMovie:
				if (!iconListCanvas.IsPlayingMovie)
				{
					state = AdvertizeState.WaitMovieEndAnimation;
				}
				break;
			case AdvertizeState.WaitMovieEndAnimation:
				if (!iconListCanvas.IsBusy)
				{
					state = AdvertizeState.WaitCanMove;
				}
				break;
			case AdvertizeState.WaitCanMove:
				if (iconListCanvas.CanSelect)
				{
					iconListCanvas.MoveNext();
					state = AdvertizeState.WaitMove;
				}
				break;
			case AdvertizeState.WaitMove:
				if (!iconListCanvas.IsMoving)
				{
					state = AdvertizeState.StartMovie;
				}
				break;
			}
			yield return null;
		}
	}

	private void PlayMovie()
	{
		iconListCanvas.StartAnimation(IconListCanvas.AnimationType.ShowMovie, OnStartMovieAnimationEnd, OnAnimationError);
		mainCanvas.StartAnimation(MainCanvasAnimation.AnimationType.HideInfoAndGuidePanel, IsAdvertize, OnAnimationError);
	}

	private void StopMovie()
	{
		iconListCanvas.StopMovie();
		iconListCanvas.StartAnimation(IconListCanvas.AnimationType.EndMovie, iconListCanvas.ShowNewIcon, OnAnimationError);
		mainCanvas.StartAnimation(MainCanvasAnimation.AnimationType.ShowInfoAndGuidePanel, showMessage: false, OnAnimationError);
	}

	private void CancelPlayMovie()
	{
		if (iconListCanvas.IsEnableMovieWindow)
		{
			StopMovie();
		}
		else
		{
			isCancelPlayMovie = true;
		}
	}

	private void OnAnimationError(string message)
	{
		message = message + "[isCancelPlayMovie : " + isCancelPlayMovie + "]\n";
		message = message + "[InputInfo : " + inputInfo.ToString() + "]\n";
		string message2 = "Animation state error occured.\n" + message;
		daemonMain.AbaasLog.PutErrorMessage(message2);
		UnityEngine.SceneManagement.SceneManager.LoadScene(UnityEngine.SceneManagement.SceneManager.GetActiveScene().name);
	}
}
