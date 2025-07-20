// renderer.js

import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { VRMLoaderPlugin } from '@pixiv/three-vrm';

window.addEventListener('DOMContentLoaded', () => {

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({
        canvas: document.querySelector('#canvas'),
        alpha: true
    });

    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    camera.position.set(0, 1.2, 0.7);

    const light = new THREE.DirectionalLight(0xffffff, 1);
    light.position.set(1, 1, 1).normalize();
    scene.add(light);
    const ambientLight = new THREE.AmbientLight(0xcccccc, 1);
    scene.add(ambientLight);

    const loader = new GLTFLoader();
    loader.register((parser) => new VRMLoaderPlugin(parser));
    const modelPath = '/hatsune_miku.vrm';

    let currentVrm = null;
    let audioListener, audio, audioAnalyser;
    
    const mouse = new THREE.Vector2();
    window.addEventListener('mousemove', (event) => {
        mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
        mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
    });

    loader.load(modelPath, (gltf) => {
        currentVrm = gltf.userData.vrm;
        scene.add(currentVrm.scene);
        console.log('Model loaded successfully!');

        // Set up the lookAt target AFTER the model is loaded
        if (currentVrm.lookAt) {
            currentVrm.lookAt.target = camera;
        }

        audioListener = new THREE.AudioListener();
        camera.add(audioListener);
        audio = new THREE.Audio(audioListener);
        audioAnalyser = new THREE.AudioAnalyser(audio, 32);

    });
    
    const clock = new THREE.Clock();

    function animate() {
        const delta = clock.getDelta();
        
        // IMPORTANT: Add a check to make sure currentVrm is not null
        if (currentVrm) {
            // Update look-at logic only if the model and lookAt are ready
            if (currentVrm.lookAt && currentVrm.lookAt.target) {
                const raycaster = new THREE.Raycaster();
                raycaster.setFromCamera(mouse, camera);
                const lookAtTarget = new THREE.Vector3().copy(raycaster.ray.direction).multiplyScalar(5).add(camera.position);
                currentVrm.lookAt.target.position.copy(lookAtTarget);
            }
            updateLipSync();
            currentVrm.update(delta); // Update all model animations
        }
        
        renderer.render(scene, camera);
    }
    renderer.setAnimationLoop(animate);
    
    function updateLipSync() {
        // Add a check here as well
        if (audioAnalyser && currentVrm && currentVrm.expressionManager) {
            const freq = audioAnalyser.getAverageFrequency();
            if (freq > 10) {
                const mouthValue = (Math.sin(Date.now() / 100) + 1) / 4 + 0.1;
                currentVrm.expressionManager.setValue('aa', mouthValue);
            } else {
                currentVrm.expressionManager.setValue('aa', 0);
            }
        }
    }

    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });
    
    const chatInput = document.getElementById('chat-input');
    const sendButton = document.getElementById('send-button');

    sendButton.addEventListener('click', async () => {
        const message = chatInput.value;
        if (!message) return;
        chatInput.value = '';
        
        try {
            const chatResponse = await fetch('http://localhost:5000/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message }),
            });
            const chatData = await chatResponse.json();
            const aiText = chatData.response;

            const speechResponse = await fetch('http://localhost:5000/synthesize-speech', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: aiText }),
            });

            if (!speechResponse.ok) {
                throw new Error(`Speech server responded with status: ${speechResponse.status}`);
            }

            const audioBlob = await speechResponse.blob();
            const audioUrl = URL.createObjectURL(audioBlob);
            
            const audioLoader = new THREE.AudioLoader();
            audioLoader.load(audioUrl, (buffer) => {
                if (audio.isPlaying) audio.stop();
                audio.setBuffer(buffer);
                audio.play();
            });

        } catch (error) {
            console.error('An error occurred:', error);
        }
    });
});