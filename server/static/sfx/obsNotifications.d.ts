import * as OBSWebSocket from 'obs-websocket-js';

export interface TransitionBegin {
	/**
	 * Duration of the transition in milliseconds.
	 */
	duration: number;
	/**
	 * The name of the transition.
	 */
	name: string;
	/**
	 * Name of the scene it's transitioning from.
	 */
	fromScene: string;
	/**
	 * Name of the scene it's transitioning to.
	 */
	toScene: string;
	/**
	 * Formatted timestamp of the stream that the transition started.
	 */
	streamTimecode: string;
}

export declare function transitionBegin(data: TransitionBegin): OBSWebSocket;